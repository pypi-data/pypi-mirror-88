# Object-oriented healpy wrapper with support for multi-resolutions maps

import healpy as hp

import HealpixMap as hmap

import matplotlib.pyplot as plt

import operator

from copy import copy,deepcopy

from astropy.io import fits
from astropy.table import Table

import numpy as np
from numpy import array, log2, sqrt

import collections

from .healpix_base import HealpixBase

class HealpixMap(HealpixBase):
    """
    Object-oriented healpy wrapper with support for multi-resolutions maps 
    (known as multi-order coverage map, or MOC).

    You can instantiate a map by providing either:
    
    * Size (through ``order`` or ``nside``), and a ``scheme`` ('RING' or 'NESTED').
      This will initialize an empty map.
    * A list of UNIQ pixels. This will initialize a MOC map. Providing the 
      values for each pixel is optional, zero-initialized by default.
    * An array (in ``data``) and an a scheme ('RING' or 'NESTED'). This will
      initialize the contents of the single-resolution map.
    * A HealpixBase object. The data will be zero-initialized.

    .. warning::
        The initialization input is not validated by default. Consider calling 
        `is_mesh_valid()` after initialization, otherwise results might be
        unexpected.


    Regardless of the underlaying grid, you can operate on maps using 
    ``*``, ``/``, ``+``, ``-``, ``**``, ``==`` and ``abs``. For binary 
    operations the result always corresponds to the finest grid, so there
    is no loss of information. If any of the operands is a MOC, the result is a
    MOC with an appropiate updated grid.. If both operands have the same NSIDE, 
    the scheme of the result corresponds to the left operand. If you want to 
    preserve the grid for a specific operand, use ``*=``, `/=`, etc. 

    .. warning::
        Information might degrade if you use in-place operators (e.g. ``*=``, `/=`)

    The maps are array-like, that is, the can be casted into a regular numpy 
    array (as used by healpy), are iterable (over the pixel values) and can be
    used with built-in function such as ``sum`` and ``max``.

    You can also access the value of pixels using regular numpy indexing 
    with ``[]``. For MOC maps, no specific pixel ordering is guaranted. For a 
    given pixel number ``ipix`` in the current grid, you can get the 
    corresponding UNIQ pixel number using ``m.pix2uniq(ipix)``.

    Args:
        data (array): Values to initialize map. Zero-initialized it not provided.
            The map NSIDE is deduced from the array size, unless ``uniq`` 
            is specified in which case this is considered a multi-resolution map.
        uniq (array or HealpixBase): List of NUNIQ pixel number to initialize a MOC map. 
        order (int): Order of HEALPix map.
        nside (int): Alternatively, you can specify the NSIDE parameter.
        scheme (str): Healpix scheme. Either 'RING', 'NESTED' or 'NUNIQ'
        base (HealpixBase): Specify the grid using a HealpixBase object
        density (bool): Whether the value of each pixel should be treated as
            counts in a histogram (``False``) or as the value of a [density]
            function evaluated at the center of the pixel (``True``). This affect 
            operations involving the splitting of a pixel. 
        dtype (array): Numpy data type. Will be ignored if data is provided.
    """

    def __init__(self,
                 data = None,
                 uniq = None,
                 order = None,
                 nside = None,
                 scheme = 'ring',
                 base = None,
                 density = False,
                 dtype = None):
        """
        Initialize an empty (use either nside or order) or initialized 
        """

        if data is not None:
            # Initializes map contents

            # Initialize base
            if uniq is not None or base is not None:
                #MOC
                
                super().__init__(uniq = uniq, base = base)

                if len(data) != self.npix:
                    raise ValueError("Data size mismatch.")
                
            else:
                # Single resolution. From array size itself
                
                nside = hp.npix2nside(len(data))

                super().__init__(nside = nside,
                                 scheme = scheme)

            # Set data
            self._data = array(data)

        else:
            # Empty map
            
            super().__init__(uniq = uniq,
                             order = order,
                             nside = nside,
                             scheme = scheme,
                             base = base)
        
            self._data = np.zeros(self.npix, dtype=dtype)

        # Other properties
        self._density = density
            
    @classmethod
    def read_map(cls, filename, field = None, uniq_field = 0, hdu = 1,
                 density = False):
        """
        Read a HEALPix map from a FITS file.

        Args:
            filename (Path): Path to file
            field (int): Column where the map contents are. Default: 0 for 
                single-resolution maps, 1 for MOC maps.
            uniq_field (int): Column where the UNIQ pixel numbers are. 
                For MOC maps only. 
            hdu (int): The header number to look at. Starts at 0.
            density (bool): Whether this is a histogram-like or a density-like map.
        
        Return:
            HealpixMap
        """

        with fits.open(filename) as hdul:

            hdu = hdul[hdu]

            scheme = hdu.header["ORDERING"]

            if scheme == 'NUNIQ':
                # Is MOC

                if field is None:
                    field = 1

                uniq = hdu.data.field(uniq_field).ravel()
                contents = hdu.data.field(field).ravel()

                m = cls(contents, uniq, density = density)

            else:
                # Sigle resolution

                if field is None:
                    field = 0

                m = cls(hdu.data.field(field).ravel(), scheme=scheme)

        return m

    def write_map(self,
                  filename,
                  extra_maps = None,
                  column_names = None,
                  extra_header = None,
                  overwrite = False,
                  coordsys = 'C'):
        """
        Write map to disc.

        Args:
            filename (Path): Path to output file
            extra_maps (HealpixMap or array): Save more maps in the same file
                as extra columns. Must be conformable.
            column_names (str or array): Name of colums. Must have the same 
                length as the number for maps. Defaults to 'CONTENTSn', where 
                ``n`` is the map number (ommited for a single map). For MOC maps,
                the pixel information is always stored in the first column, called
                'UNIQ'.
            coordsys (str): Coordinate system. Celestial (`'C'`), Galactic (`'G'`)
                or Ecliptic (`'E'`)
            extra_header (iterable): Iterable of (keyword, value, [comment]) tuples
            overwrite (bool): If True, overwrite the output file if it exists. 
                Raises an OSError if False and the output file exists. 
        """
        
        # Standarize data for astropy's Table
        if self.is_moc:

            # IVOA specifies pixels must be in ascending UNIQ order
            usort = np.argsort(self._uniq)
            data = [self._uniq[usort], self._data[usort]]

        else:

            data = [self._data]

        # Add extra maps
        if extra_maps is not None:
            
            if isinstance(extra_maps, HealpixMap):
                extra_maps = (extra_maps,)

            for map in extra_maps:

                if not self.conformable(map):
                    raise ValueError("All extra maps must be conformable")

                if map.is_moc:
                    data.append(map._data[usort])
                else:
                    data.append(map._data)

        # Column names
        nmaps = len(data) - self.is_moc
        
        if column_names is not None:

            if isinstance(column_names, str):
                column_names = [column_names]
            
            if len(column_names) != nmaps:
                raise ValueError("Colum names must match the number of maps.")
            
        else:

            if nmaps > 1:

                column_names = ["CONTENTS{}".format(i) for i in range(nmaps)]
                
            else:

                column_names = ["CONTENTS"]

        if self.is_moc:

            column_names.insert(0, 'UNIQ')

        # Header
        header = [('PIXTYPE', 'HEALPIX',
                       'HEALPIX pixelisation'),
                  ('ORDERING', self.scheme,
                       'Pixel ordering scheme: RING, NESTED, or NUNIQ'),
                  ('COORDSYS', coordsys,
                       'Celestial (C), Galactic (G) or Ecliptic (E)'),
                  ('NSIDE', self.nside,
                       'Resolution parameter of HEALPIX'),
                  ('INDXSCHM', 'EXPLICIT' if self.is_moc else 'IMPLICIT',
                       'Indexing: IMPLICIT or EXPLICIT')]

        if self.is_moc:
            header.extend([('MOCORDER', self.order, 'Best resolution order')])
        
        if extra_header is not None:
            header.extend(extra_header)
        
        # Prepare table and write
        table = Table(data, names = column_names)

        hdu = fits.table_to_hdu(table)

        hdu.header.extend(header)

        hdulist = fits.HDUList([fits.PrimaryHDU(), hdu])

        hdulist.writeto(filename, overwrite = overwrite)
        
    @classmethod
    def adaptive_moc_mesh(cls, max_nside, split_fun, density = False,
                      dtype = None):
        """
        Return a zero-initialized MOC map, with an adaptive resolution
        determined by an arbitrary function.

        Args:
            max_nside (int): Maximum HEALPix nside to consider
            split_fun (function): This method should return ``True`` if a pixel 
            should be split into pixel of a higher order, and ``False`` otherwise. 
            It takes two integers, ``start`` (inclusive) and ``stop`` (exclusive), 
            which correspond to a single pixel in nested rangeset format for a 
            map of nside ``max_nside``.
            density (bool): Will be pass to HealpixMap initialization.
            dtype (dtype): Data type

        Return:
            HealpixMap
        """
        
        base = HealpixBase.adaptive_moc_mesh(max_nside, split_fun)

        return cls(np.zeros(base.npix, dtype = dtype),
                   base._uniq,
                   density = density)
        
    @classmethod
    def moc_from_pixels(cls, nside, pixels, nest = False, density = False,
                        dtype = None):
        """
        Return a zero-initialize MOC map where a list of pixels are kept at a 
        given nside, and every other pixel is appropiately downsampled.
        
        Also see the more generic ``adaptive_moc_mesh()``.

        Args:
            nside (int): Maximum healpix NSIDE (that is, the NSIDE for the pixel order
                list) 
            pixels (array): Pixels that must be kept at the finest pixelation
            nest (bool): Whether the pixels are a 'NESTED' or 'RING' scheme
            density (bool): Wheather the map is density-like or histogram-like
            dtype: Daty type
        """

        base = HealpixBase.moc_from_pixels(nside, pixels, nest = nest)

        return cls(np.zeros(base.npix, dtype = dtype),
                   base._uniq,
                   density = density)

    @classmethod
    def moc_histogram(cls, nside, samples, max_value, nest = False, weights = None):
        """
        Generate an adaptive MOC map by histogramming samples. 

        If the number of samples is greater than the number of pixels in a map
        of the input ``nside``, consider generating a single-resolution
        map and then use `to_moc()`.

        Also see the more generic ``adaptive_moc_mesh()``.

        Args: 
            nside (int): Healpix NSIDE of the samples and maximum NSIDE of the 
                output map
            samples (int array): List of pixels representing the samples. e.g.
                the output of `healpy.ang2pix()`.
            max_value: maximum number of samples (or sum of weights) per pixel.
                Note that due to limitations of the input ``nside``, the output
                could contain pixels with a value largen than this
            nest (bool): Whether the samples are in NESTED or RING scheme
            weights (array): Optionally weight the samples. Both must have the
                same size.
        
        Return:
            HealpixMap
        """

        # Standarize samples
        if not nest:
            samples = array([hp.ring2nest(nside, pix) for pix in samples])


        if weights:
            samples = np.rec.fromarrays([samples, weights],
                                        names = ['pix', 'wgt'])

        else:
            samples = np.rec.fromarrays([samples],
                                 names = ['pix'])

        samples.sort(order = 'pix')

        # Get empty mesh by reusing adaptive_moc_mesh
        def value_fun(start, stop):

            start_pos, stop_pos = np.searchsorted(samples.pix, [start, stop])

            if weights:
                value = sum(samples.wgt[start_pos:stop_pos])
            else:
                value = stop_pos - start_pos

            return value
                
        if weights:
            dtype = array(weights).dtype
        else:
            dtype = int
        
        moc_map = cls.adaptive_moc_mesh(nside,
                                        lambda i,f: value_fun(i,f) > max_value,
                                        density = False,
                                        dtype = dtype)

        # Fill
        rangesets = moc_map.pix_rangesets(nside)

        for pix,(start,stop) in enumerate(rangesets):
            
            moc_map[pix] = value_fun(start, stop)

        return moc_map

        
    def to_moc(self, max_value):
        """
        Convert a single-resolution map into a MOC based on the maximum value
        a given pixel the latter should have. 

        ... note:: 
            
            The maximum nside of the MOC map is the same as the nside of the 
            single-resolution map, so the output map could contain pixels with 
            a value greater than this.

        If the map is already a MOC map, it will recompute the grid accordingly
        by combining uniq pixels. Uniq pixels are never split. 

        Also see the more generic ``adaptive_moc_mesh()``.

        Args:
            max_value: Maximum value per pixel of the MOC. Whether the map is
                histogram-like or density-like is taken into account.

        Return:
            HealpixMap
        """

        # Get empty mesh by reusing adaptive_moc_mesh
        if self.is_moc or self.is_ring:
            # MOC map, will work in rangesets
            
            rs = self.pix_rangesets(self.nside)
            rs_argsort = np.argsort(rs.start)

            def _nest2pix(start,stop):
                # Same as nest2pix but avoids recomputing the rangesets and sorting
                
                return  np.searchsorted(rs.start, [start,stop],
                                        sorter = rs_argsort)

                
            def value_fun(start, stop):

                start_pos, stop_pos = _nest2pix(start, stop)

                pix = rs_argsort[start_pos:stop_pos]

                if self._density:
                    # Weighted average
                    value = sum((rs.stop[pix]-rs.start[pix])*self._data[pix])
                    value /= rs.stop[stop_pos-1] - rs.start[start_pos]
                else:
                    # Simple sum
                    value = sum(self._data[pix])

                return value
                    
            def split_fun(start,stop):

                start_pos, stop_pos = _nest2pix(start, stop)

                if stop_pos - start_pos == 1:
                    # A single pixel, don't split
                    return False
                else:

                    pix = rs_argsort[start_pos:stop_pos]
                    
                    if self._density:
                        return max(self._data[pix]) > max_value

                    else:
                        return sum(self._data[pix]) > max_value
                    
        else:
            # Single resolution map
            
            def value_fun(start, stop):
                value = sum(self._data[start:stop])

                if self._density:
                    value /= stop-start

                return value

            def split_fun(start, stop):
                if self._density:
                    return max(self._data[start:stop]) > max_value
                else:
                    return value_fun(start,stop) > max_value

        moc_map = self.adaptive_moc_mesh(self.nside,
                                         split_fun,
                                         density = self._density,
                                         dtype = self.dtype)

        # Fill
        rangesets = moc_map.pix_rangesets(self.nside)

        for pix,(start,stop) in enumerate(rangesets):
            
            moc_map[pix] = value_fun(start, stop)

        return moc_map

    def density(self, density = None, update = True):
        """
        Switch between a density-like map and a histogram-like map.

        Args:
            density (bool or None): Whether the value of each pixel should be treated as
                counts in a histogram (``False``) or as the value of a [density]
                function evaluated at the center of the pixel (``True``). This affect 
                operations involving the splitting of a pixel. ``None`` will leave 
                this paramter unchanged.
            update (bool): If True, the values of the map will be updated accordingly.
                Otherwise only the density parameter is changed.

        Return:
            bool: The current density

        """
        if density is not None:

            if self._density != density:

                self._density = density

                if update:
                    
                    if density:
                        # From histogram-like to density-like
                        for pix in range(self.npix):
                            self[pix] /= np.diff(self.pix2range(self.nside, pix))

                    else:
                        # From density-like to histogram-like
                        for pix in range(self.npix):
                            self[pix] *= np.diff(self.pix2range(self.nside, pix))

        return self._density

    @property
    def data(self):
        """
        Get the raw data in the form of an array.
        """

        return self._data
        
    @property
    def dtype(self):
        return self._data.dtype
        
    def __eq__(self, other):

        return (self.conformable(other) and
                np.array_equal(self._data, other._data) and
                self._density == other._density)
                
    def __getitem__(self, key):

        return self._data[key]
        
    def __setitem__(self, key, value):

        self._data[key] = value
        
    def __imul__(self, other):

        return self._ioperation(other, operator.imul)

    def __mul__(self, other):

        return self._operation(other, operator.mul)

    def __rmul__(self, other):

        return self._roperation(other, operator.mul)

    def __itruediv__(self, other):

        return self._ioperation(other, operator.itruediv)

    def __truediv__(self, other):

        return self._operation(other, operator.truediv)

    def __rtruediv__(self, other):

        return self._roperation(other, operator.truediv)

    def __ifloordiv__(self, other):

        return self._ioperation(other, operator.ifloordiv)

    def __floordiv__(self, other):

        return self._operation(other, operator.floordiv)

    def __rfloordiv__(self, other):

        return self._roperation(other, operator.floordiv)

    def __iadd__(self, other):

        return self._ioperation(other, operator.iadd)

    def __add__(self, other):

        return self._operation(other, operator.add)

    def __radd__(self, other):
            
        return self._roperation(other, operator.add)

    def __isub__(self, other):

        return self._ioperation(other, operator.isub)

    def __sub__(self, other):

        return self._operation(other, operator.sub)

    def __rsub__(self, other):
 
        return self._roperation(other, operator.sub)

    def __ipow__(self, other):

        return self._ioperation(other, operator.ipow)

    def __pow__(self, other):

        return self._operation(other, operator.pow)

    def __neg__(self):

        new = deepcopy(self)

        new._data *= -1

        return new

    def __abs__(self):

        new = deepcopy(self)

        new._data = np.abs(new._data)
        
        return new
    
    def __array__(self):

        return self._data
        
    def rasterize(self, nside, scheme):
        """
        Convert to map of a given NSIDE and scheme

        Args:
            nside (int): HEALPix NSIDE
            scheme (str): RING or NESTED

        Return:
            HealpixMap
        """

        scheme = scheme.upper()
        
        if scheme not in ['RING', 'NESTED']:
            raise ValueError("Scheme must be RING or NESTED")

        if self.nside == nside and self.scheme == scheme:
            # Same grid, nothing to do
            
            return deepcopy(self)

        else:
            # All other case can be handled with the identity operation
            
            raster = HealpixMap(nside = nside,
                                scheme = scheme,
                                density = self._density)

            raster._ioperation(self, lambda a,b: b)

            return raster

    def _roperation(self, other, operation):

        if not np.isscalar(other):
            raise ValueError("Operations can only occur between maps or a "
                             "map and a scalar")

        m = deepcopy(self)

        m._data = operation(other, m._data)

        return m
        
    def _operation(self, map1, operation):

        # If second is not a map (e.g. scalar or array), we'll keep the grid
        # If any map is MOC, result will be MOC. Grid is updated.
        # If both are single-resolution, result will have the finest grid
        # If both are single resolution and same order, scheme will correspond
        # to first operand
        # If maps are conformable, the output grid remains unchanged

        map0 = self
        
        if np.isscalar(map1):
            # Operation by a scalar

            map0 = deepcopy(map0)
            return map0._ioperation(map1, operation)

        else:

            # Operation by another map

            # Cast to HealpixMap if needed
            if not isinstance(map1, HealpixMap):
                raise ValueError("Operations can only occur between maps or a "
                                 "map and a scalar")

            # Optimize for different cases
            if (map0.is_moc or map1.is_moc) and not map0.conformable(map1):
                
                # Multi-resolution map
                # This will change the underlaying NUNIQ grid

                # Convert pixel numbers to an equivalent sorted list of nested
                # rangeset for highest posible order
                max_nside = max(map0.nside, map1.nside)

                rs0 = map0.pix_rangesets(max_nside)
                rs1 = map1.pix_rangesets(max_nside)

                sort0 = np.argsort(rs0.start)
                sort1 = np.argsort(rs1.start)

                # Initialize new data with highest possible number of pixels,
                # some will be discarded at the end but this is fasten than append
                new_uniq = np.zeros(map0.npix + map1.npix, dtype = int)
                new_data = np.zeros(map0.npix + map1.npix, dtype = map0._data.dtype)

                pos0 = 0
                pos1 = 0

                pix_new = 0

                start = 0 # Rangeset start of new pixel

                while pos0 < map0.npix and pos1 < map1.npix:

                    # Get input values
                    pix0   = sort0[pos0]
                    range0 = rs0[pix0]
                    value0 = map0[pix0] 

                    pix1   = sort1[pos1]
                    range1 = rs1[pix1]
                    value1 = map1[pix1]
                    
                    stop = min(range0.stop, range1.stop) # Rangeset stop of new pixel

                    # Handle density maps
                    npix_new = stop - start

                    if not map0._density:
                        npix_ratio0 = npix_new / (range0.stop-range0.start)
                        value0 = value0 * npix_ratio0

                    if not map1._density:
                        npix_ratio1 = npix_new / (range1.stop-range1.start)
                        value1 = value1 * npix_ratio1

                    # Operation
                    value = operation(value0, value1)

                    new_uniq[pix_new] = hmap.range2uniq(max_nside,
                                                        (start, stop))
                    new_data[pix_new] = value

                    # Advance to next pixel
                    pix_new += 1

                    if stop == range0.stop:
                        pos0 += 1

                    if stop == range1.stop:
                        pos1 += 1

                    start = stop

                # Update density parameter
                # If any of the maps is histogram-like, the result is also a
                # weighted histogram-like map
                new_density = map0._density and map1._density

                # Create new map
                return HealpixMap(new_data[:pix_new],
                                  new_uniq[:pix_new],
                                  density = new_density)
                
            else:

                # Single-resolution or conformable, can reuse in-place operation
                
                if map1.order > map0.order:
                    map0,map1 = map1,map0

                map0 = deepcopy(map0)
                    
                return map0._ioperation(map1, operation)

    
    def _ioperation(self, map1, operation):

        map0 = self
        
        if np.isscalar(map1):
            # Operation by a scalar

            map0._data = operation(map0._data, map1)

        else:

            # Operation by another map or something that can be turned into a map

            # Cast to HealpixMap if needed
            if not isinstance(map1, HealpixMap):
                raise ValueError("Operations can only occur between maps or a "
                                 "map and a scalar")

            # Optimize procedure for various situations
            if map0.conformable(map1):
                # Same underlaying grid, so easy operation

                map0._data = operation(map0._data, map1._data)

            elif ((map0.is_moc or map1.is_moc) or
                  ((map0.is_ring or map1.is_ring) and map0.order != map1.order)):

                # There is no clear optimization in this case
                # Will work in the rangeset representation

                max_nside = max(map0.nside, map1.nside)

                rs0   = map0.pix_rangesets(max_nside)
                sort0 = np.argsort(rs0.start)
                pos0  = 0

                rs1   = map1.pix_rangesets(max_nside)
                sort1 = np.argsort(rs1.start)
                pos1  = 0

                while pos0 < map0.npix and pos1 < map1.npix:

                    pix0 = sort0[pos0]
                    range0 = rs0[pix0]
                    len0 = range0.stop - range0.start

                    pix1 = sort1[pos1]
                    range1 = rs1[pix1]
                    len1 = range1.stop - range1.start

                    if len0 > len1:
                        # Downgrade pix1 by getting summing over child pixels
                        # (or weighted average, for a density map)

                        value0 = map0[pix0]
                        value1 = 0

                        while True:
                            # Will break when we catch up with map0

                            if map1._density:
                                # Will take the weighted average
                                value1 += len1 * map1[pix1]
                            else:
                                # Simple sum
                                value1 += map1[pix1]

                            if range0.stop == range1.stop:
                                break

                            pos1   += 1
                            pix1   = sort1[pos1]
                            range1 = rs1[pix1]
                            len1   = range1.stop - range1.start

                        if map1._density:
                            value1 /= len0

                        map0[pix0] = operation(value0, value1)

                    else:

                        # Upgrade pix1 by dividing it up
                        # (or simply getting the value for density)

                        while True:
                            # Will break when we catch up with map1

                            value1 = map1[pix1]

                            if not map1._density:
                                value1 /= len1 // len0

                            value0 = map0[pix0]

                            map0[pix0] = operation(value0, value1)

                            if range0.stop == range1.stop:
                                break

                            pos0   += 1
                            pix0   = sort0[pos0]
                            range0 = rs0[pix0]
                            len0   = range0.stop - range0.start

                    pos0 += 1
                    pos1 += 1
                
                
            elif map0.order == map1.order:
                # Same order, different scheme, single-resolution

                nside = map0.nside

                if map0.scheme == 'NESTED':
                    # map1 is RING, map0 is NESTED

                    for pix in range(map0.npix):

                        map0[pix] = operation(map0[pix],
                                              map1[hp.nest2ring(nside, pix)])

                else:
                    # map1 is NESTED, map0 is RING

                    for pix in range(map0.npix):

                        map0[pix] = operation(map0[pix],
                                              map1[hp.ring2nest(nside, pix)])

            else:

                # Only possibility left is that both are NESTED with different
                # order, which is easy to handle

                if map1.order > map0.order:
                    # Downgrade map1 by summing or getting the weighted average

                    npix_ratio = int(4**(map1.order - map0.order))

                    for pix in range(map0.npix):

                        value1 = sum(map1._data[pix*npix_ratio:(pix+1)*npix_ratio])

                        if map1._density:
                            value1 /= npix_ratio

                        map0._data[pix] = operation(map0._data[pix], value1)

                else:

                    # Upgrade map1 by splitting the pixel
                    # (or just use the value if density)

                    npix_ratio = int(4**(map0.order - map1.order))

                    for pix in range(map1.npix):

                        value1 = map1._data[pix]

                        if not map1._density:
                            value1 /= npix_ratio

                        pix0_start = pix*npix_ratio
                        pix0_stop = pix0_start + npix_ratio

                        map0._data[pix0_start: pix0_stop] = \
                            operation(map0._data[pix0_start: pix0_stop],
                                      value1)

            # Update density parameter
            # If any of the maps is histogram-like, the result is also a
            # weighted histogram-like map
            map0._density = map0._density and map1._density

        return map0

    def plot(self,
             ax = None,
             proj = 'moll',
             rot=0,
             coord='C',
             flip='astro',
             xsize=800,
             ysize=None,
             lonra=[-180,180],
             latra=[-90,90],
             half_sky=False,
             reso=1.5,
             **kwargs):
        """
        Plot map. This is a wrapper for matplotlib.pyplot.imshow

        Plots of multi-resolution maps are equivalent to plotting the equivalent
        rasterized single-resolution map --i.e. values are weighted based on pixel area.
        
        Args:
            ax (matplotlib.axes.Axes): Axes on where to plot the map. If ``None``,
                it will create a new figure.
            proj (str): Projections: 'moll' (molltweide), 'cart' (carthographic), 
                'orth' (orthographics) or 'gnom' (gnomonic)
            rot (float or sequence): Describe the rotation to apply. In the 
                form (lon, lat, psi) (unit: degrees) : the point at longitude 
                lon and latitude lat will be at the center. An additional 
                rotation of angle psi around this direction is applied. If a 
                scalar, the rotation is performed around zenith
            coord (str): Either one of ‘G’ (Galactic), ‘E’ (Equatorial) or 
                ‘C’ (Celestial) to describe the 
                coordinate system of the map, or a sequence of 2 of these to 
                rotate the map from the first to the second coordinate system.
            flip (str): Defines the convention of projection : ‘astro’ 
                (east towards left, west towards right) or ‘geo’ (east towards 
                right, west towards left)
            xsize (int): The horizontal size of the image.
            ysize (int): The verital size of the image. For carthographic and 
                gnomonic projections only.
            lonra (array): Range in longitude (degrees). For carthographic only. 
            latra (array): Range in latitude (degrees). For carthographic only.
            half_sky (bool): Plot only one side of the sphere. For orthographic 
                only
            reso (float): Resolution (in arcmin). For gnominic projection only.
            **kwargs: Passed to matplotlib.pyplot.imshow

        Return:
           AxesImage, healpix.projector.SphericalProj: The first return value
               corresponds to the output ``imgshow``. The second is the healpy's
               projector used. This is particularly useful to add extra elements
               to the plots, e.g.::

                   plot, proj = m.plot(ax, 'moll')
                   x,y = proj.ang2xy(np.deg2rad(90), np.deg2rad(45))
                   ax.text(x, y, "(zenith = 90 deg, azimuth = 45 deg)")
        """

        # Create axes if needed
        default_plot = False
        if ax is None:
            plt.figure(figsize=(8.5, 5.4))        
            ax = plt.gca()
            ax.axis('off')
            default_plot = True
            
        # Get appropiate projector
        projector = self._get_projector(proj, rot, coord, flip, xsize, ysize,
                                        lonra, latra, half_sky, reso)
        
        # Get values
        class rasterizer:
            """
            This is a wrapper around [], that will divide the value of the pixel
            if the map is MOC and histogram-like. This will give the same result 
            as calling rasterize() first and then plotting the equivalent 
            single-resolution map
            """
            
            def __init__(self, map):
                self.map = map
            
            def __getitem__(self, pix):

                if self.map.is_moc and not self.map._density:

                    # Histogram-like MOC, will divide the pixel
                    pix_nside = hmap.uniq2nside(self.map._uniq[pix]) 

                    pix_order = log2(pix_nside)
                    
                    npix_ratio = 4 ** (self.map.order - pix_order)

                    return  self.map[pix] / npix_ratio
                    
                else:

                    # Single resolution or density MOC, nothing to do
                    
                    return self.map[pix]
                
        img = projector.projmap(rasterizer(self),
                                self.vec2pix,
                                coord=coord)

        # Plot
        plot =  ax.imshow(img,
                          extent = projector.get_extent(),
                          origin="lower",
                          **kwargs)

        if default_plot:
            plt.gcf().colorbar(plot, orientation="horizontal")
        
        return plot, projector

    def get_interp_val(self, theta, phi):
        """
        Return the bi-linear interpolation value of a map using 4 nearest neighbours.

        For MOC maps, this is equivalent to raterizing the map first to the 
        highest order.

        Args:
            theta (float or array): Zenith angle (rad)
            phi (float or array): Azimuth angle (rad)

        Return:
            scalar or array
        """

        pixels,weights = self.get_interp_weights(theta, phi)

        values = self[pixels]
            
        if self.is_moc and not self._density:
            # Split the pixels up to corresponding maximum order
            
            nside = hmap.uniq2nside(self._uniq[pixels])
            
            npix_ratio =  int(4**self.order) / nside / nside
            
            values = values / npix_ratio

        return np.matmul(weights, values)

    def moc_sort(self):
        """
        Sort the uniq pixels composing a MOC map based on its 
        rangeset representation
        """

        if not self.is_moc:
            return

        rs = self.pix_rangesets(self.nside)

        rs_argsort = np.argsort(rs.start)

        self._uniq = self._uniq[rs_argsort]
        self._data = self._data[rs_argsort]

