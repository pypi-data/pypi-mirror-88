# Based on information gathered from:
# https://github.com/StuartLittlefair/dcimg/blob/master/dcimg/Raw.py
# hamamatsuOrcaTools: https://github.com/orlandi/hamamatsuOrcaTools
# Python Microscopy: http://www.python-microscopy.org
#                    https://bitbucket.org/david_baddeley/python-microscopy

# Author: Giacomo Mazzamuto <mazzamuto@lens.unifi.it>

"""This module provides the `DCIMGFile` class for accessing Hamamatsu DCIMG
files."""

import math
import logging
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__version__ = '0.6.0'


class DCIMGFile(object):
    """A DCIMG file (Hamamatsu format), memory-mapped.

    This class provides an interface for reading 3D Hamamatsu DCIMG files.

    Usage is pretty straightforward. First of all, create a `DCIMGFile` object:

    >>> my_file = DCIMGFile('input_file.dcimg')
    >>> my_file
    <DCIMGFile shape=2450x2048x2048 dtype=<class 'numpy.uint16'>\
file_name=input_file.dcimg>

    Image data can then be accessed using NumPy's basic indexing:

    >>> my_file[-10, :5, :5]
    array([[101, 104, 100,  99,  89],
           [103, 102, 103,  99, 102],
           [101, 104,  99, 108,  98],
           [102, 111,  99, 111,  95],
           [103,  98,  99, 104, 106]], dtype=uint16)

    Other convenience methods for accessing image data are: `zslice`,
    `zslice_idx`, `frame` and `whole`.

    `DCIMGFile` supports context managers:

    >>> with DCIMGFile('input_file.dcimg') as f:
    >>>     a = f[800, ...]


    .. seealso:: NumPy's basic indexing: `numpy:arrays.indexing`

    """

    FILE_HDR_DTYPE = [
        ('file_format', 'S8'),
        ('format_version', '<u4'),  # 0x08
        ('skip', '5<u4'),           # 0x0c
        ('nsess', '<u4'),           # 0x20 ?
        ('nfrms', '<u4'),           # 0x24
        ('header_size', '<u4'),     # 0x28 ?
        ('skip2', '<u4'),           # 0x2c
        ('file_size', '<u8'),       # 0x30
        ('skip3', '2<u4'),          # 0x38
        ('file_size2', '<u8'),      # 0x40, repeated
    ]

    SESS_HDR_DTYPE = [
        ('session_size', '<u8'),  # including footer
        ('skip1', '6<u4'),
        ('nfrms', '<u4'),
        ('byte_depth', '<u4'),
        ('skip2', '<u4'),
        ('xsize', '<u4'),
        ('bytes_per_row', '<u4'),
        ('ysize', '<u4'),
        ('bytes_per_img', '<u4'),
        ('skip3', '2<u4'),
        ('offset_to_data', '<u4'),
        ('session_data_size', '<u8'),  # header_size + x*y*byte_depth*nfrms
    ]

    SESSION_FOOTER_DTYPE = [
        ('format_version', '<u4'),
        ('skip0', '<u4'),
        ('offset_to_2nd_struct', '<u8'),
        ('skip1', '2<u4'),
        ('offset_to_offset_to_end_of_data', '<u8'),
        ('skip2', '2<u4'),
        ('footer_size', '<u4'),
        ('skip3', '<u4'),

        # an almost empty part after the footer
        # contains 'offset_to_end_of_data', 0x00000000 0x00000000
        # repeated 2 * nfrms times
        ('2nd_footer_size', '<u4'),  # = 2 * nfrms * 16

        ('skip4', '19<u4'),
        ('offset_to_end_of_data', '<u8'),  # sum of the two offsets above
        ('skip5', '<u8'),  # sum of the two offsets above
        ('offset_to_end_of_data_again', '<u8'),  # repeated
        ('skip6', '<u8'),  # repeated
    ]

    SESSION_FOOTER2_DTYPE = [
        ('offset_to_offset_to_timestamps', '<u8'),
        ('skip0', '2<u4'),
        ('offset_to_offset_to_frame_counts', '<u8'),
        ('skip1', '2<u4'),
        ('offset_to_offset_to_4px', '<u8'),
        ('skip2', '2<u4'),
        ('offset_to_frame_counts', '<u8'),
        ('skip3', '2<u4'),
        ('offset_to_timestamps', '<u8'),
        ('skip4', '4<u4'),
        ('offset_to_4px', '<u8'),
        ('skip5', '<u4'),
        ('4px_offset_in_frame', '<u4'),

        # this is zero if there is no 4px correction info in the footer
        # (maybe because of cropping, so the first line is not included) and
        # is 8 if there is 4px correction info stored in the footer. Might be
        # the size in bytes of the 4px correction for each frame (8 = 4 * 2)
        ('4px_size', '<u8'),
    ]

    # newer versions of the dcimg format have a different header
    NEW_SESSION_HEADER_DTYPE = [
        ('session_size', '<u8'),
        ('skip1', '13<u4'),
        ('nfrms', '<u4'),
        ('byte_depth', '<u4'),
        ('skip2', '<u4'),
        ('xsize', '<u4'),
        ('ysize', '<u4'),
        ('bytes_per_row', '<u4'),
        ('bytes_per_img', '<u4'),
        ('skip3', '2<u4'),
        ('offset_to_data', '<u8'),
    ]

    NEW_FRAME_FOOTER_DTYPE = [
        ('progressive_number', '<u4'),
        ('timestamp', '<u4'),
        ('timestamp_frac', '<u4'),
        ('4px', '<u8'),
        ('zeros', '<u12'),
    ]

    NEW_CROP_INFO = [
        ('x0', '<u2'),
        ('xsize', '<u2'),
        ('y0', '<u2'),
        ('ysize', '<u2'),
    ]

    FMT_OLD = 1
    FMT_NEW = 2

    def __init__(self, file_path=None):
        self.mm = None
        """a `numpy.memmap` object with the raw contents of the DCIMG file."""
        self.mma = None
        """memory-mapped `numpy.ndarray` of the image data, without 4px
        correction."""
        self._deep_copy_enabled = None

        self._file_header = None
        self._sess_header = None
        self._sess_footer = None
        self._sess_footer2 = None
        self._ts_data = None  #: timestamp data
        self._fs_data = None  #: framestamp data
        self.file_path = file_path
        if file_path:
            self.file_path = Path(file_path)
        self.fmt_version = None
        self.x0 = 0
        self.y0 = 0
        self.binning = 1
        self._target_line = -1  #: target line for 4px correction

        self.first_4px_correction_enabled = True
        """For some reason, the first 4 pixels of each frame (or the first 4
        pixels of line number 1023 of each frame) are stored in a different
        area in the file. This switch enables retrieving those 4 pixels. If
        False, those pixels are set to 0. If None, they are left unchanged.
        Defaults to True."""

        self._4px = None
        """A `numpy.ndarray` of shape (`nfrms`, 4) containing the first 4
        pixels of each frame."""

        if file_path is not None:
            self.open()

    def __repr__(self):
        return '<DCIMGFile file_path="{}" shape={} dtype={}>'.format(
            self.file_path, self.shape, self.dtype)

    def __del__(self):
        self.close()

    def __enter__(self):
        self.deep_copy_enabled = True
        return self

    def __exit__(self, *args):
        self.close()

    @property
    def deep_copy_enabled(self):
        return self._deep_copy_enabled

    @deep_copy_enabled.setter
    def deep_copy_enabled(self, value):
        self._deep_copy_enabled = value

    @property
    def file_size(self):
        """File size in bytes."""
        return self._file_header['file_size'][0]

    @property
    def nfrms(self):
        """Number of frames (Z planes), same as `zsize`."""
        return self._sess_header['nfrms'][0]

    @property
    def byte_depth(self):
        """Number of bytes per pixel."""
        return self._sess_header['byte_depth'][0]

    @property
    def dtype(self):
        """NumPy numerical dtype."""
        if self.byte_depth == 1:
            return np.dtype(np.uint8)
        elif self.byte_depth == 2:
            return np.dtype(np.uint16)

    @property
    def xsize(self):
        return self._sess_header['xsize'][0]

    @property
    def ysize(self):
        return self._sess_header['ysize'][0]

    @property
    def zsize(self):
        return self.nfrms

    @property
    def bytes_per_row(self):
        return self._sess_header['bytes_per_row'][0]

    @property
    def bytes_per_img(self):
        return self._sess_header['bytes_per_img'][0]

    @property
    def shape(self):
        """Shape of the whole image stack.

        Returns
        -------
        tuple
            (`zsize`, `ysize`, `xsize`)
        """
        return self.nfrms, self.ysize, self.xsize

    @property
    def _header_size(self):
        return self._file_header['header_size'][0]

    @property
    def _session_footer_offset(self):
        sess_data_size = None
        if self.fmt_version == self.FMT_OLD:
            sess_data_size = int(self._sess_header['session_data_size'][0])
        elif self.fmt_version == self.FMT_NEW:
            sess_data_size = \
                self._sess_header['offset_to_data'][0] \
                + (int(self._sess_header['bytes_per_img'][0] + 8) * self.nfrms)
        return self._header_size + sess_data_size

    def open(self, file_path=None):
        self.close()
        if file_path is not None:
            self.file_path = Path(file_path)

        self.mm = np.memmap(self.file_path, mode='r')

        try:
            self._parse_header()
            self._parse_footer()
        except ValueError:
            self.close()
            raise

        bd = self.byte_depth
        data_strides = None
        data_offset = (int(self._file_header['header_size'])
                       + int(self._sess_header['offset_to_data']))
        if self.fmt_version == self.FMT_OLD:
            if self._has_4px_data:
                offset = self._session_footer_offset \
                         + int(self._sess_footer2['offset_to_4px'])
                self._4px = np.ndarray(
                    (self.nfrms, 4), self.dtype, self.mm, offset)
            data_strides = (self.bytes_per_img, self.bytes_per_row, bd)
        elif self.fmt_version == self.FMT_NEW:
            strides = (self.bytes_per_img + 32, bd)
            self._4px = np.ndarray((self.nfrms, 4), self.dtype, self.mm,
                                   data_offset + self.bytes_per_img + 12,
                                   strides)
            padding = self.bytes_per_img - self.xsize * self.ysize * bd
            padding //= self.ysize
            data_strides = (self.bytes_per_img + 32,
                            self.xsize * bd + padding,
                            bd)

        self.mma = np.ndarray(self.shape, self.dtype, self.mm,
                              data_offset, data_strides)

        if self.fmt_version == DCIMGFile.FMT_OLD:
            # framestamp offset
            offset = int(self._session_footer_offset + 272)
            self._fs_data = np.ndarray(self.nfrms, np.uint32, self.mm, offset)

            # timestamp offset
            offset += 4 * self.nfrms
            self._ts_data = np.ndarray(
                (self.nfrms, 2), np.uint32, self.mm, offset)
        elif self.fmt_version == DCIMGFile.FMT_NEW:
            # framestamps
            offset = int(self._file_header['header_size']
                         + self._sess_header['offset_to_data'][0]
                         + self.bytes_per_img)
            strides = self.bytes_per_img + 32
            self._fs_data = np.ndarray(
                self.nfrms, np.uint32, self.mm, offset, strides)

            # timestamps
            offset += 4
            strides = (self.bytes_per_img + 32, 4)
            self._ts_data = np.ndarray(
                (self.nfrms, 2), np.uint32, self.mm, offset, strides)

        self.compute_target_line()

    def compute_target_line(self):
        if self.fmt_version == DCIMGFile.FMT_OLD:
            if self._has_4px_data:
                self._target_line = (
                    int(self._sess_footer2['4px_offset_in_frame'])
                    // self.bytes_per_row)
            else:
                self._target_line = -1
        else:
            self._target_line = (1023 - self.y0) // self.binning

    def close(self):
        self.mm = None  # Close the memmap.

    def _parse_header(self):
        self._file_header = np.ndarray((1,), self.FILE_HDR_DTYPE, self.mm)

        if not self._file_header['file_format'] == b'DCIMG':
            raise ValueError('Invalid DCIMG file')

        if self._file_header['format_version'] == 0x7:
            sess_dtype = self.SESS_HDR_DTYPE
            self.fmt_version = self.FMT_OLD
        elif self._file_header['format_version'] == 0x1000000:
            self.fmt_version = self.FMT_NEW
            sess_dtype = self.NEW_SESSION_HEADER_DTYPE
        else:
            raise ValueError('Invalid DCIMG format version: 0x{:04x}'.format(
                self._file_header['format_version'][0]))

        self._sess_header = np.ndarray((1,), sess_dtype, self.mm,
                                       offset=self._header_size)

        if self.fmt_version == self.FMT_NEW:
            i = self._header_size + 712
            crop_info = np.ndarray((1,), self.NEW_CROP_INFO, self.mm, i)

            self.x0 = crop_info['x0']
            self.y0 = crop_info['y0']
            binning_x = crop_info['xsize'][0] // self.xsize
            binning_y = crop_info['ysize'][0] // self.ysize

            if binning_x != binning_y:
                raise ValueError('different binning in X and Y')

            self.binning = binning_x

        if self.byte_depth != 1 and self.byte_depth != 2:
            raise ValueError(
                "Invalid byte-depth: {}".format(self.byte_depth))

        if self.bytes_per_img != self.bytes_per_row * self.ysize:
            e_str = 'invalid value for bytes_per_img'
            raise ValueError(e_str)

    def _parse_footer(self):
        if self.fmt_version != self.FMT_OLD:
            return

        self._sess_footer = np.ndarray((1,), self.SESSION_FOOTER_DTYPE, self.mm,
                                       self._session_footer_offset)

        offset = (self._session_footer_offset
                  + int(self._sess_footer['offset_to_2nd_struct']))

        self._sess_footer2 = \
            np.ndarray((1,), self.SESSION_FOOTER2_DTYPE, self.mm, offset)

    @property
    def _has_4px_data(self):
        """
        Whether the footer contains 4px correction (only for `FMT_OLD`)

        Returns
        -------
        bool
        """
        if self.fmt_version == self.FMT_NEW:
            raise NotImplementedError('not implemented for FMT_NEW')

        # maybe this is sufficient
        # return int(self._sess_footer2['4px_size']) > 0

        footer_size = int(self._sess_footer['footer_size'])
        offset_to_4px = int(self._sess_footer2['offset_to_4px'])

        return footer_size == offset_to_4px + 4 * self.byte_depth * self.nfrms

    def __getitem__(self, item):
        """Allow to access image data using NumPy's basic indexing."""
        a = self.mma[item]

        if self.deep_copy_enabled:
            a = np.copy(a)

        if self.first_4px_correction_enabled is None:
            return a

        if a.size == 0:
            return a

        # ensure item is a tuple
        if isinstance(item, list):
            item = tuple(item)
        else:
            item = np.index_exp[item]

        # ensure all items are slice objects
        myitem = []
        for i in item:
            if isinstance(i, int):
                start = i
                stop = i + 1
                step = 1
            elif i is Ellipsis:
                for _ in range(0, 3 - len(item) + 1):
                    myitem.append(slice(0, self.shape[len(myitem)], 1))
                continue
            elif isinstance(i, slice):
                start = i.start
                stop = i.stop
                step = i.step if i.step is not None else 1
            else:
                raise TypeError("Invalid type: {}".format(type(i)))

            curr_max = self.shape[len(myitem)]
            if start is None:
                start = 0 if step > 0 else curr_max
            elif start < 0:
                start += curr_max
                if stop is not None:
                    stop += curr_max
            elif start > curr_max:
                start = curr_max

            if stop is None:
                stop = curr_max if step > 0 else 0
            elif stop < 0:
                stop += curr_max
            elif stop > curr_max:
                stop = curr_max

            myitem.append(slice(start, stop, step))

        for _ in range(0, 3 - len(myitem)):
            myitem.append(slice(0, self.shape[len(myitem)], 1))

        startx = myitem[2].start
        stopx = myitem[2].stop
        stepx = myitem[2].step

        starty = myitem[1].start
        stopy = myitem[1].stop
        stepy = myitem[1].step

        target_line = self._target_line
        condition_y = False
        if self.fmt_version == self.FMT_OLD and self._has_4px_data:
            condition_y = starty == 0 or stopy == 0
        elif self.fmt_version == self.FMT_NEW:
            if stepy > 0:
                condition_y = starty <= target_line <= stopy
            elif stepy < 0:
                condition_y = stopy <= target_line <= starty

        if condition_y and ((0 <= startx < 4) or stopx < 4):
            if a.size == 1:
                if self.first_4px_correction_enabled:
                    a = self._4px[myitem[0].start, startx]
                else:
                    a = 0
                return a

            if startx < stopx:
                newstartx = 0
                if stopx > 4:
                    newstopx = int(math.ceil((4 - startx) / abs(stepx)))
                else:
                    newstopx = (stopx - startx) // abs(stepx)
            else:
                newstopx = a.shape[-1]
                if a.shape[-1] < 4:
                    newstartx = 0
                else:
                    newstartx = (a.shape[-1] - 4 // abs(stepx))

            if newstartx == newstopx:
                return np.empty([0])

            newshape = [math.ceil(
                (myitem[i].stop - myitem[i].start) / myitem[i].step)
                for i in range(0, 3)]

            old_shape = a.shape

            a.shape = newshape

            newy = int(math.floor((target_line - starty) / stepy))
            if stepy < 0:
                newy -= 1

            a_index_exp = np.index_exp[..., newy, newstartx:newstopx]

            if not a.flags.writeable:
                a = np.copy(a)

            if self.first_4px_correction_enabled:
                _range = sorted((startx, stopx))
                _4start = max(0, _range[0])
                _4stop = min(4, _range[1])
                _4px = self._4px[item[0], _4start:_4stop:abs(stepx)]

                if stepx < 0:
                    _4px = _4px[..., ::-1]
                a[a_index_exp] = _4px
            else:
                a[a_index_exp] = 0

            a.shape = old_shape

        return a

    @property
    def framestamps(self):
        """Framestamps of all frames.

        Returns
        -------
        `numpy.ndarray`
            A numpy array of dtype `numpy.uint32` with framestamps.
        """
        return self._fs_data

    @property
    def timestamps(self):
        """Timestamps of all frames.

        Returns
        -------
        `numpy.ndarray`
            A numpy array of dtype `numpy.datetime64` with frame timestamps.
        """
        return np.asarray([self.ts(i) for i in range(self.nfrms)])

    def ts(self, frame):
        """
        Timestamp of a single frame.

        Parameters
        ----------
        frame : int
            Frame index

        Returns
        -------
        `numpy.datetime64`
        """
        whole = int.from_bytes(self._ts_data[frame, 0], 'little')
        fraction = int.from_bytes(self._ts_data[frame, 1], 'little')
        return np.datetime64(whole * 10**6 + fraction, 'us')

    @staticmethod
    def _args_to_slice(arg1, arg2=None, step=None):
        myslice = slice(arg1, arg2, step)
        if arg2 is None and step is None:
            myslice = slice(arg1)
        return myslice

    def zslice(self, arg1, arg2=None, step=None, dtype=None, copy=True):
        """Return a slice along `Z`, i.e.\  a substack of frames.

        Parameters
        ----------
        arg1 : int
            Mandatory argument, will be passed to `python:slice`
            If arg2 and step are both None, it will be passed as `slice(arg1)`,
            i.e. it would act as the stop argument.
        arg2 : int
            If not null, will be passed as `slice(arg1, arg2, step)`
        step : int
            If not null, will be passed as `slice(arg1, arg2, step)`
        dtype
        copy : bool
            If True, the requested slice is copied to memory. Otherwise a
            memory mapped array is returned.

        Returns
        -------
        `numpy.ndarray`
            A numpy array of the original type or of `dtype`, if specified. The
            shape of the array is (`end_frame` - `start_frame`, `ysize`,
            `xsize`).
        """
        old_copy = self.deep_copy_enabled
        self.deep_copy_enabled = copy
        myslice = self._args_to_slice(arg1, arg2, step)
        a = self[myslice.start:myslice.stop:myslice.step]
        if dtype is not None:
            a = a.astype(dtype)
        self.deep_copy_enabled = old_copy

        return a

    def zslice_idx(self, index, frames_per_slice=1, dtype=None, copy=True):
        """Return a slice, i.e.\  a substack of frames, by index.

        Parameters
        ----------
        index : int
            slice index
        frames_per_slice : int
            number of frames per slice
        dtype
        copy : see `zslice`

        Returns
        -------
        `numpy.ndarray`
            A numpy array of the original type or of `dtype`, if specified. The
            shape of the array is  (`frames_per_slice`, `ysize`, `xsize`).
        """
        start_frame = index * frames_per_slice
        end_frame = start_frame + frames_per_slice
        return self.zslice(start_frame, end_frame, 1, dtype, copy)

    def whole(self, dtype=None, copy=True):
        """Convenience function to retrieve the whole stack.

        Equivalent to call `zslice_idx` with `index` = 0 and
        `frames_per_slice` = `nfrms`

        Parameters
        ----------
        dtype
        copy : see `zslice`

        Returns
        -------
        `numpy.ndarray`
            A numpy array of the original type or of dtype, if specified. The
            shape of the array is `shape`.
        """
        return self.zslice_idx(0, self.nfrms, dtype, copy)

    def frame(self, index, dtype=None, copy=True):
        """Convenience function to retrieve a single frame (Z plane).

        Same as calling `zslice_idx` and squeezing.

        Parameters
        ----------
        index : int
            frame index
        dtype
        copy : see `zslice`

        Returns
        -------
        `numpy.ndarray`
            A numpy array of the original type or of `dtype`, if specified. The
            shape of the array is (`ysize`, `xsize`).
        """
        return np.squeeze(self.zslice_idx(index, dtype=dtype, copy=copy))
