# Pixelization related function for single resolutions maps

import healpy as hp

import numpy as np
from numpy import array

def order2npix(order):
    """
    Get the number of pixel for a map of a given order

    Args:
        order (int or array)

    Return:
        int or array
    """

    return 12*4**array(order, dtype=int)

# healpy functions not related to the grid , copied here just for convenience
vec2ang = hp.vec2ang
"""
Same as healpy.pixelfunc.vec2ang. Included here for convinience. 
"""

ang2vec = hp.ang2vec
"""
Same as healpy.pixelfunc.ang2vec. Included here for convinience. 
"""

