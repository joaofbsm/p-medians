#!/usr/bin/env python3

"""Utility functions"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import math

def euclidean_distance(a, b):
    """2D euclidian distance calculation
    
    Arguments:
        a -- First point in 2D space.
        b -- Second point in 2D space.
    """

    return math.sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2))
