#!/usr/bin/env python3

"""Solution components for the p-medians problem"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import math


class Solution:
    def __init__(self, distance=None, medians=[], association=None):
        self.distance = distance
        self.medians = medians
        self.association = association
        