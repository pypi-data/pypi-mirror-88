
import healpy as hp

import HealpixMap as hmap

import numpy as np
from numpy import array, log2, sqrt

import matplotlib.pyplot as plt

class HealpixBase:
    """
    Basic operations related to HEALPix pixelization, for which the map
    contents information is not needed. This class is conceptually very similar 
    the the Healpix_Base class of Healpix_cxx.

    Single resolution maps are fully defined by specifying their order 
    (or NSIDE) and ordering scheme ("RING" or "NESTED"). 

    Multi-resolution maps follow an explicit "NUNIQ" scheme, with each pixel 
    identfied by a _uniq_ number. No specific is needed nor guaranteed.

    .. warning::
        The initialization input is not validated by default. Consider calling 
        `is_mesh_valid()` after initialization, otherwise results might be
        unexpected.


    Args:
        uniq (array): Explicit numbering of each pixel in an "NUNIQ" scheme.
        order (int): Order of HEALPix map.
        nside (int): Alternatively, you can specify the NSIDE parameter.
        scheme (str): Healpix scheme. Either 'RING', 'NESTED' or 'NUNIQ'
        base (HealpixBase): Alternatively, you can copy the properties of another
            HealpixBase object
    """

    def __init__(self,
                 uniq = None,
                 order = None,
                 nside = None,
                 base = None,
                 scheme = 'ring'):

        if base is not None:
            # Copy another HealpixBase
            
            self._uniq = base._uniq
            self._scheme = base._scheme
            self._order = base._order

        elif uniq is not None:
            # MOC map
            
            self._uniq = array(uniq, dtype = int)
            
            # Scheme and order are implicit
            self._scheme = "NUNIQ"
            
            self._order = hp.nside2order(hmap.uniq2nside(max(uniq)))
            
        else:
            # Single resolution map

            self._uniq = None
            
            # User specified nside instead of order
            if nside is not None:
                
                if order is not None:
                    raise ValueError("Specify either 'order' or 'nside'")
                
                order = hp.nside2order(nside)

            if order is None:
                raise ValueError("Specifcy nside or order")
                
            self._order = order

            if scheme is None:
                    raise ValueError("Specify scheme")

            self._scheme = scheme.upper()

            if self._scheme not in ['RING','NESTED', 'NUNIQ']:
                raise ValueError("Scheme can only be 'ring', 'nested' or 'NUNIQ'")


    def __eq__(self, other):

        return self.conformable(other)
            
    @classmethod
    def adaptive_moc_mesh(cls, max_nside, split_fun):
        """
        Return a MOC mesh with an adaptive resolution
        determined by an arbitrary function.

        Args:
            max_nside (int): Maximum HEALPix nside to consider
            split_fun (function): This method should return ``True`` if a pixel 
            should be split into pixel of a higher order, and ``False`` otherwise. 
            It takes two integers, ``start`` (inclusive) and ``stop`` (exclusive), 
            which correspond to a single pixel in nested rangeset format for a 
            map of nside ``max_nside``.

        Return:
            HealpixBase
        """

        map_uniq = array([], dtype = int)

        max_order = hp.nside2order(max_nside)
        order_list = array(range(max_order+1))
        nside = 2**order_list
        npix_ratio = 4 ** (max_order - order_list)
        uniq_shift = 4 * nside * nside
        npix_ratio = 4 ** (max_order - order_list)

        start_buffer = np.zeros((max_order+1, 4), dtype=int)
        cursor = -np.ones((max_order+1), dtype=int)

        for base_pix in range(12):

            order = 0
            start_buffer[order][0] = base_pix * npix_ratio[order]
            cursor[order] = 0

            while order >= 0:

                if cursor[order] < 0:
                    order -= 1
                    continue

                start = start_buffer[order][cursor[order]]
                stop  = start + npix_ratio[order]

                cursor[order] -= 1

                if order < max_order and split_fun(start, stop):
                    # Split

                    order += 1

                    split_shift = array(range(4))*npix_ratio[order]
                    start_buffer[order] = start + split_shift

                    cursor[order] = 3

                else:
                    # Add to map

                    uniq = (start / npix_ratio[order] + uniq_shift[order]).astype(int) 

                    map_uniq = np.append(map_uniq, uniq)

        return cls(map_uniq)

    @classmethod
    def moc_from_pixels(cls, nside, pixels, nest = False):
        """
        Return a MOC mesh where a list of pixels are kept at a 
        given nside, and every other pixel is appropiately downsampled.
        
        Also see the more generic ``adaptive_moc()`` and ``adaptive_moc_mesh()``.

        Args:
            nside (int): Maximum healpix NSIDE (that is, the NSIDE for the pixel
                list) 
            pixels (array): Pixels that must be kept at the finest pixelation
            nest (bool): Whether the pixels are a 'NESTED' or 'RING' scheme
        """

        # Always work in nested
        if not nest:
            pixels = array([hp.ring2nest(nside, pix) for pix in pixels])
            
        # Auxiliary function so we can reuse adaptive_moc_mesh()
        pixels.sort()
        
        def pix_list_range_intersect(start, stop):

            start_index,stop_index = np.searchsorted(pixels, [start,stop])

            return start_index < stop_index

        # Get the grid        
        return cls.adaptive_moc_mesh(nside,
                                     pix_list_range_intersect)

    def conformable(self, other):
        """
        For single-resolution maps, return ``True`` if both maps have the same
        nside and scheme.

        For MOC maps, return `True` if both maps have the same list of UNIQ 
        pixels (including the ordering)
        """

        if self.is_moc:
            return np.array_equal(self._uniq, other._uniq)
        else:
            return (self._order == other._order and 
                    self._scheme == other._scheme)

    @property
    def npix(self):
        """
        Get number of pixels.

        For multi-resolutions maps, this corresponds to the number of utilized 
        UNIQ pixels.

        Return:
            int
        """

        if self.is_moc:   
            return len(self._uniq)
        else:
            return int(12 * 4**self._order)

    @property
    def order(self):
        """
        Get map order

        Return:
            int
        """
        
        return self._order

    @property
    def nside(self):
        """
        Get map NSIDE

        Return:
            int
        """

        return int(2**self.order)
        
    @property
    def scheme(self):
        """
        Return HEALPix scheme
        
        Return:
            str: Either 'NESTED', 'RING' or 'NUNIQ'
        """

        return self._scheme

    @property
    def is_nested(self):
        """
        Return true if scheme is NESTED or NUNIQ
        
        Return
            bool
        """

        return self._scheme == "NESTED" or self._scheme == 'NUNIQ'
        
    @property
    def is_ring(self):
        """
        Return true if scheme is RING
        
        Return
            bool
        """

        return self._scheme == "RING"

    @property
    def is_moc(self):
        """
        Return true if this is a Multi-Dimensional Coverage (MOC) map 
        (multi-resolution)

        Return:
            bool
        """

        return self._uniq is not None

    def pix_rangesets(self, nside = None):
        """
        Get the equivalent range of `child pixels` in nested scheme for a map 
        of equal or higher nside

        Args:
            nside (int or None): Nside of output range sets. If None, the map
                nside will be used

        Return:
            recarray: With columns named 'start' (inclusive) and 
                'stop' (exclusive) 
        """

        if nside is None:
            nside = self.nside
        
        start, stop = self.pix2range(nside, range(self.npix))
        
        return np.rec.fromarrays([start,stop], names = ['start', 'stop'])

    def pix_order_list(self):
        """
        Get a list of lists containing all pixels sorted by order

        Return:
           (list, list): (``pix_per_order``, ``nest_pix_per_order``)
               Each list has a size equal to the map order. 
               Each element is a list of all pixels whose order
               matches the index of the list position.
               The first output contains the index of the pixels, while the
               second contains their coresponding pixel number in a nested scheme.
        """

        pix_per_order = [[] for _ in range(self.order+1)]
        nest_pix_per_order = [[] for _ in range(self.order+1)]

        for pix in range(self.npix):

            nside, nest_pix = hmap.uniq2nest(self.pix2uniq(pix))

            order = hp.nside2order(nside)

            pix_per_order[order].append(pix)
            nest_pix_per_order[order].append(nest_pix)

        return pix_per_order,nest_pix_per_order
    
    def pix2range(self, nside, pix):
        """
        Get the equivalent range of `child pixels` in nested scheme for a map 
        of equal or higher nside
        
        Args:
            nside (int): Nside of output range sets
            pix (int or array): Pixel numbers
            
        Return:
            (int or array, int or array): Start pixel (inclusive) and 
                stop pixel (exclusive) 
        """
        
        if self.is_moc:

            return hmap.uniq2range(nside, self._uniq[pix])

        else:

            if self.is_ring:
                pix = hp.ring2nest(self.nside, pix)
                
            return hmap.nest2range(self.nside, pix, nside)

    def pixarea(self, pix = 0):
        """
        Return area of pixel in steradians

        Args:
            pix (int or array): Pixel number. Only relevant for MOC maps
        
        Return:
            float or array
        """

        if self.is_moc:
            nside = hmap.uniq2nside(self._uniq[pix])
        else:
            nside = self.nside

        return 1.047197551196597746 / nside / nside
        
    def pix2ang(self, pix):
        """
        Return the coordinates of the center of a pixel
        
        Args:
            pix (int or array)

        Return:
            (float or array, float or array)
        """

        if self.is_moc:

            nside, pix = hmap.uniq2nest(self.pix2uniq(pix))

            return hp.pix2ang(nside, pix, nest = True)
            
        else:
            return hp.pix2ang(self.nside, pix, nest = self.is_nested)
            
    def pix2vec(self, pix):
        """
        Return a vector corresponding to the center of a pixel
        
        Args:
            pix (int or array)

        Return:
            array: Size (3,N)
        """

        if self.is_moc:

            nside, pix = hmap.uniq2nest(self.pix2uniq(pix))

            return hp.pix2vec(nside, pix, nest = True)
            
        else:
            return hp.pix2vec(self.nside, pix, nest = self.is_nested)
            
    def ang2pix(self, theta, phi):
        """
        Get the pixel (as used in []) that contains a given coordinate

        Args:
            theta (float or array): Zenith angle
            phi (float or arrray): Azimuth angle
      
        Return:
            int or array
        """

        pixels = hp.ang2pix(self.nside, theta, phi, nest=self.is_nested)
        
        if self.is_moc:
            pixels = self.nest2pix(pixels)
            
        return pixels
            
    def vec2pix(self, x, y, z):
        """
        Get the pixel (as used in []) that contains a given coordinate

        Args:
            theta (float or array): Zenith angle
            phi (float or arrray): Azimuth angle
      
        Return:
            int or array
        """

        pixels = hp.vec2pix(self.nside, x, y, z, nest=self.is_nested)

        if self.is_moc:
            pixels = self.nest2pix(pixels)
            
        return pixels
        
    def pix2uniq(self, pix):
        """
        Get the UNIQ representation of a given pixel index.

        Args:
            pix (int): Pixel number in the current scheme (as used for [])
        """

        if self.is_moc:

            return self._uniq[pix]

        else:

            if self.scheme == 'RING':
                pix = hp.ring2nest(self.nside, pix)

            return hmap.nest2uniq(self.nside, pix)

    @property    
    def uniq(self):
        """
        Get an array with the NUNIQ numbers for all pixels
        """

        if self.is_moc:
            return self._uniq
        else:
            return self.pix2uniq(range(self.npix))
        
    def nest2pix(self, pix):
        """
        Get the corresponding pixel in the current grid for a pixel in NESTED
        scheme. For MOC map, return the pixel that contains it. 

        Args:
            pix (int or array): Pixel number in NESTED scheme. Must correspond 
                to a map of the same order as the current.

        Return:
            int or array
        """

        if self.is_moc:

            # Work with rangesets for maximum order,
            # then find pixel number for this order,
            # and then find the rangesets that contain these pixels

            rangesets = self.pix_rangesets(self.nside)
            
            rs_argsort = np.argsort(rangesets.stop)
            
            ipix = np.searchsorted(rangesets.stop, pix,
                                   side = 'right',
                                   sorter = rs_argsort)

            opix = rs_argsort[ipix]

            # Follow healpy convention for null pix
            if np.ndim(opix) == 0:
                if pix == -1:
                    opix = -1
            else:
                opix[pix == -1] = -1
                
            return opix
            
        else:
            
            if self.is_nested:
                return pix
            else:
                return hp.nest2ring(self.nside, pix)
            
    
    def get_interp_weights(self, theta, phi):
        """
        Return the 4 closest pixels on the two rings above and below the 
        location and corresponding weights. Weights are provided for bilinear 
        interpolation along latitude and longitude

        Args:
            theta (float or array): Zenith angle (rad)
            phi (float or array): Azimuth angle (rad)
 
        Return:
            tuple: (pixels, weights), each with of (4,) if the input is scalar,
                if (4,N) where N is size of
                theta and phi. For MOC maps, these pixel numbers might repeate.
        """

        pixels,weights = hp.get_interp_weights(self.nside, theta, phi,
                                               nest = self.is_nested)

        if self.is_moc:
            pixels = self.nest2pix(pixels)

        return (pixels, weights)
            
    def get_all_neighbours(self, theta, phi = None):
        """
        Return the 8 nearest pixels. For MOC maps, these might repeat, as this
        is equivalent to raterizing the maps to the highest order, getting the 
        neighbohrs, and then finding the pixels tha contain them.

        Args:
            theta (float or int or array): Zenith angle (rad). If phi is 
                ``None``, these are assummed to be pixels numbers. For MOC maps,
                these are assumed to be pixel numbers in NESTED scheme for the
                equivalent single-resolution map of the highest order.
            phi (float or array or None): Azimuth angle (rad)

        Return:
            array: pixel number of the SW, W, NW, N, NE, E, SE and S neighbours,
                shape is (8,) if input is scalar, otherwise shape is (8, N) if 
                input is of length N. If a neighbor does not exist (it can be 
                the case for W, N, E and S) the corresponding pixel number will 
                be -1.
        """
        
        neighbors = hp.get_all_neighbours(self.nside, theta, phi,
                                          nest = self.is_nested)

        if self.is_moc:
            neighbors = self.nest2pix(neighbors)

        return neighbors
 
    def is_mesh_valid(self):
        """
        Return ``True`` is the map pixelization is valid. For
        single resolution this simply checks that the size is a valid NSIDE value.
        For MOC maps, it checks that every point in the sphere is covered by
        one and only one pixel.
        
        Return:
            True
        """

        if self.is_moc:

            # Work in rangesets, and check that there is no gap in between them
            rs = self.pix_rangesets(self.nside)

            rs.sort(order = 'start')

            return (rs.start[0] == 0 and
                    rs.stop[-1] == hp.nside2npix(self.nside) and
                    np.array_equal(rs.start[1:], rs.stop[:-1]))
            
        else:
                
            return hp.isnpixok(self.npix)

    def _pix_query_fun(self, fun):
        """
        Return a wrapper for healpy's pix querying routines

        Args:
            fun (function): Healpy's query_* functions
        
        Return:
            function: With apprpiate grid, passes rest of arguments to fun
        """

        def wrapper(*args, **kwargs):

            if self.is_moc:

                # We'll do it order by order

                pix_per_order, nest_pix_per_order = self.pix_order_list()
                
                query_pix = np.zeros(0, dtype = int)

                for order in range(self.order+1):

                    pixels = fun(hp.order2nside(order), nest = True,
                                 *args, **kwargs)

                    query_bool = np.isin(nest_pix_per_order[order], pixels)

                    order_pix = array(pix_per_order[order], dtype=int)

                    query_pix = np.append(query_pix,
                                          order_pix[query_bool])

                return np.sort(query_pix)
                        
            else:

                return fun(self.nside, nest = self.is_nested,
                           *args, **kwargs)

        return wrapper                

    def query_polygon(self, vertices, inclusive=False, fact=4):
        """
        Returns the pixels whose centers lie within the convex polygon defined 
        by the vertices array (if inclusive is False), or which overlap with 
        this polygon (if inclusive is True).

        Args:
            vertices (float): Vertex array containing the vertices of the 
                polygon, shape (N, 3).
            inclusive (bool): f False, return the exact set of pixels whose 
                pixels centers lie within the region; if True, return all 
                pixels that overlap with the region.
            fact (int): Only used when inclusive=True. The overlapping test 
                will be done at the resolution fact*nside. For NESTED ordering, 
                fact must be a power of 2, less than 2**30, else it can be any 
                positive integer. Default: 4.
            
        Return:
            int array: The pixels which lie within the given polygon.
        """
        
        fun = self._pix_query_fun(hp.query_polygon)

        return fun(vertices, inclusive=inclusive, fact=fact)

    def query_disc(self, vec, radius, inclusive=False, fact=4):
        """

        Args:
            vec (float, sequence of 3 elements): The coordinates of unit vector 
                defining the disk center.
            radius (float): The radius (in radians) of the disk
            inclusive (bool): f False, return the exact set of pixels whose 
                pixels centers lie within the region; if True, return all 
                pixels that overlap with the region.
            fact (int): Only used when inclusive=True. The overlapping test 
                will be done at the resolution fact*nside. For NESTED ordering, 
                fact must be a power of 2, less than 2**30, else it can be any 
                positive integer. Default: 4.
        
        Return:
            int array: The pixels which lie within the given disc.
        """
        
        fun = self._pix_query_fun(hp.query_disc)

        return fun(vec, radius, inclusive=inclusive, fact=fact)

    def query_strip(self,  theta1, theta2, inclusive=False):
        """
        Returns pixels whose centers lie within the colatitude range defined by 
        theta1 and theta2 (if inclusive is False), or which overlap with this 
        region (if inclusive is True). If theta1<theta2, the region between 
        both angles is considered, otherwise the regions 0<theta<theta2 and 
        theta1<theta<pi.

        Args:
            theta (float): First colatitude (radians)
            phi (float): Second colatitude (radians)
            inclusive (bool): f False, return the exact set of pixels whose 
                pixels centers lie within the region; if True, return all 
                pixels that overlap with the region.

        Return:
            int array: The pixels which lie within the given strip.
        """
        
        fun = self._pix_query_fun(hp.query_strip)

        return fun(theta1, theta2, inclusive=inclusive)
    
    def boundaries(self, pix, step = 1):
        """
        Returns an array containing vectors to the boundary of the nominated pixel.

        The returned array has shape (3, 4*step), the elements of which are the 
        x,y,z positions on the unit sphere of the pixel boundary. In order to 
        get vector positions for just the corners, specify step=1.
        """
        
        if self.is_moc:

            def single_pix_bounds(pix):

                nside, nest_pix = hmap.uniq2nest(self._uniq[pix])
    
                return hp.boundaries(nside, nest_pix, step = step, nest = True)

            moc_bounds = np.vectorize(single_pix_bounds)
            
            return moc_bounds(pix)

        else:

            return hp.boundaries(self.nside, pix, step, nest = self.is_nested)

    
    def plot_grid(self,
                  ax = None,
                  proj = 'moll',
                  step = 32,
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
        Plot the pixel boundaries of a Healpix grid

        Args:
            m (HealpixBase): Map defining the grid
            ax (matplotlib.axes.Axes): Axes on where to plot
            proj (healpy.projector.SphericalProj): Projector to converto 
                spherical coordinates to plot's axes coodinates
            step (int): How many points per pixel side
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
            **kwargs: Passed to matplotlib.pyplot.plot()
        
        Return:
            matplotlib.lines.Line2D, healpy,projector: The first return value
               corresponds to the output ``pyplot.plot()`` for one of the pixels. 
               The second is the healpy's projector used. This is particularly 
               useful to add extra elements to the plots, e.g.::

                   plot, proj = m.plot_grid(ax, 'moll')
                   x,y = proj.ang2xy(np.deg2rad(90), np.deg2rad(45))
                   ax.text(x, y, "(zenith = 90 deg, azimuth = 45 deg)")
        """

        # Get appropiate projector
        projector = self._get_projector(proj, rot, coord, flip, xsize, ysize,
                                        lonra, latra, half_sky, reso)

        # Create axes is needed
        if ax is None:
            plt.figure()        
            ax = plt.gca()
            ax.axis('off')

        # Set limits
        left, right, bottom, top = projector.get_extent()
        ax.set_xlim(left, right)
        ax.set_ylim(bottom, top)
        ax.set_aspect('equal')
        
        # Every line should have the same color
        if 'c' in kwargs:
            color = kwargs.pop('c')
        else:
            color = kwargs.pop('color', 'black')

        # Get figure size
        fig = ax.figure

        figsize = fig.get_size_inches()*fig.dpi
        
        if proj == 'cart':
            # Equivalent all-sky resolution
            figsize *= [360, 180] / np.abs([lonra[1]-lonra[0], latra[1]-latra[0]])
            
        max_res = int(np.max(figsize))
        
        # Plot boundaries as lines
        for pix in range(self.npix):

            # Get boundaries
            vec = self.boundaries(pix, step = step)

            # Close loop
            vec = np.append(vec, vec[:,0].reshape(-1,1), axis = 1)

            # Project
            x,y = projector.vec2xy(vec)

            # Remove discontinuities
            dx = np.abs(np.diff(x))
            dy = np.abs(np.diff(y))
            dist = sqrt(dx*dx + dy*dy)
            jumps = dist > 3*np.nanmedian(dist)
            jumps = np.append(jumps, False)

            if any(jumps):

                ijumps = np.nonzero(jumps)[0]+1

                x = np.insert(x, ijumps, np.nan)
                y = np.insert(y, ijumps, np.nan)

            # Plot
            plot = ax.plot(x,y, color = color, **kwargs)

        # Add map frame, where discontinuities happend
        if proj == 'moll':

            # 2:1 ellipse
            theta = np.linspace(0, 2*np.pi, 8 * step)
            x = 2 * np.cos(theta)
            y = np.sin(theta)
            
            ax.plot(x,y, color = color, **kwargs)

        elif proj == 'cart':

            # 2:1 rectangle
            x = np.linspace(-180, 180, 4 * step)
            y = np.ones(len(x))
            ax.plot(x, -90*y, color = color, **kwargs)
            ax.plot(x,  90*y, color = color, **kwargs)

            y = np.linspace(-90, 90, 3 * step)
            x = np.ones(len(y))
            ax.plot( 180*x, y, color = color, **kwargs)
            ax.plot(-180*x, y, color = color, **kwargs)

        elif proj == 'orth':

            # 1 circle per hemisphere
            theta = np.linspace(0, 2*np.pi, 6 * step)
            x = np.cos(theta)
            y = np.sin(theta)

            if half_sky:
                ax.plot(x, y, color = color, **kwargs)
            else:
                ax.plot(x-1, y, color = color, **kwargs)
                ax.plot(x+1, y, color = color, **kwargs)
            
        return plot, projector
            
    @staticmethod
    def _get_projector(proj = 'moll',
                       rot=0,
                       coord='C',
                       flip='astro',
                       xsize=800,
                       ysize=None,
                       lonra=[-180,180],
                       latra=[-90,90],
                       half_sky=False,
                       reso=1.5):
        """
        Get the appropiate healpy projector

        Args:
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


        Return:
            healpy.projector
        """

        proj = proj.lower()
        
        if proj == 'moll':            
            projector = hp.projector.MollweideProj(rot=rot,
                                                   coord=coord,
                                                   flipconv=flip,
                                                   xsize=xsize)
            
        elif proj == 'cart':

            # This shouldn't be needed IMO, but I haven't tracker down
            # where in healpy things break if it is outside -pi<-> pi
            lonra = (np.array(lonra) + 180) % 360 - 180
            
            projector = hp.projector.CartesianProj(rot=rot,
                                                   coord=coord,
                                                   flipconv=flip,
                                                   xsize=xsize,
                                                   ysize=ysize,
                                                   lonra=lonra,
                                                   latra=latra)

        elif proj == 'orth':
            projector = hp.projector.OrthographicProj(rot=rot,
                                                      coord=coord,
                                                      flipconv=flip,
                                                      xsize=xsize,
                                                      half_sky=half_sky)

        elif proj == 'gnom':
            projector = hp.projector.GnomonicProj(rot=rot,
                                                  coord=coord,
                                                  flipconv=flip,
                                                  xsize=xsize,
                                                  ysize=ysize,
                                                  reso=reso)
            
        else:
            raise ValueError("Wrong porojection")

        return projector
        
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
        
        
