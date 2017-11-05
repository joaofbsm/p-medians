#!/usr/bin/env python3

"""Utility functions"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import math
import numpy as np
from node import Node


def read_data(file_path, initial_pheromone):
    nodes = []

    with open(file_path, 'r') as f:
        n, p = tuple(map(int, f.readline().split()))

        for line in f:
            line = line.split()
            x = int(line[0])
            y = int(line[1])
            capacity = int(line[2])
            demand = int(line[3])
            node = Node(x, y, capacity, demand, initial_pheromone)
            nodes.append(node)

    return n, p, nodes


def write_data():
    pass


def euclidean_distance(a, b):
    """2D euclidian distance calculation
    
    Arguments:
        a -- First point in 2D space.
        b -- Second point in 2D space.
    """

    return math.sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2))
