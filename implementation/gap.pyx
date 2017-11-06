#!/usr/bin/env python3

"""GAP heuristic to solve the capacitated p-medians problem"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import utils
import numpy as np


def GAP(world, ant):
    """General Assignment Problem Heuristic.

    Returns the association matrix for the solution.

    Arguments:
        world -- World structural representation.
        ant -- Ant entity.
    """

    n = world.n  # Number of nodes
    p = world.p  # Number of medians
    centers = ant.medians  # Medians
    clients = list(set(np.arange(n)) - set(centers))  # Non-medians
    association = np.zeros((n, n))  # Associates nodes with medians

    # Sort clients decrescently by their demand
    ordered_clients = sorted(clients, key=lambda i: world.nodes[i].demand, 
                             reverse=True)
    for client in ordered_clients:
        # Sort centers by their distance to client
        ordered_centers = sorted(centers, 
                                 key=lambda m: world.distances[client][m])

        # Attribute client to a center
        for center in ordered_centers:
            capacity = world.nodes[center].actual_capacity

            # Attribute it to the first center with available capacity
            if capacity - world.nodes[client].demand >= 0:
                capacity -= world.nodes[client].demand
                world.nodes[center].actual_capacity = capacity
                association[client][center] = 1
                break 

    # Reset nodes capacity
    for center in centers:
        world.nodes[center].actual_capacity = world.nodes[center].capacity

    return association