#!/usr/bin/env python3

"""Utility functions"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import os
import math
import random
import numpy as np
from node import Node


def read_data(file_path):
    nodes = []

    with open(file_path, 'r') as f:
        n, p = tuple(map(int, f.readline().split()))

        for line in f:
            line = line.split()
            x = int(line[0])
            y = int(line[1])
            capacity = int(line[2])
            demand = int(line[3])
            node = Node(x, y, capacity, demand, 0.5)
            nodes.append(node)

    return n, p, nodes


def write_data(output_dir, output):
    repetitions, iterations, _ = output.shape

    os.makedirs(output_dir, exist_ok=True)

    for repetition in range(repetitions):
        file_path = "{}{}.csv".format(output_dir, repetition)
        with open(file_path, 'w') as f:
            for iteration in range(iterations):
                f.write("{}, {}, {}, {}\n".format(iteration, 
                                        output[repetition][iteration][0],
                                        output[repetition][iteration][1],
                                        output[repetition][iteration][2]))


def generate_seeds(seed, n_repetitions):
    """Generate the seeds for the repetitions according to one master seed.
    
    Arguments:
        seed -- Random seed.
        n_repetitions = Number of repetitions.
    """

    rnd_gen = random.Random(seed)

    return [rnd_gen.randint(0, 2 ** 32 - 1) for i in range(n_repetitions)]


def euclidean_distance(a, b):
    """2D euclidian distance calculation.
    
    Arguments:
        a -- First point in 2D space.
        b -- Second point in 2D space.
    """

    return math.sqrt(((a.x - b.x) ** 2) + ((a.y - b.y) ** 2))
