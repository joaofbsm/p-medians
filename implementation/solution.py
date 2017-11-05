#!/usr/bin/env python3

"""Solution components for the p-medians problem"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import math


class Solution:
    def __init__(self, distance=None, medians=[], association=None):
        """Solution constructor.
        
        Keyword arguments:
            distance -- Total solution distance (default: {None})
            medians -- Array of median nodes index (default: {[]})
            association -- Association matrix of the solution (default: {None})
        """
        
        self.distance = distance
        self.medians = medians
        self.association = association
        