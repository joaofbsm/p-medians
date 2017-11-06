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
    ordered_clients = sort_clients(world, clients)
    for client in ordered_clients:
        # Sort centers by their distance to client
        ordered_centers = sort_centers(world, client[0], centers)

        # Attribute client to a center
        for center in ordered_centers:
            capacity = world.nodes[center[0]].actual_capacity

            # Attribute it to the first center with available capacity
            if capacity - world.nodes[client[0]].demand >= 0:
                capacity -= world.nodes[client[0]].demand
                world.nodes[center[0]].actual_capacity = capacity
                association[client[0]][center[0]] = 1
                break 

    # Reset nodes capacity
    for center in centers:
        world.nodes[center].actual_capacity = world.nodes[center].capacity

    return association


def sort_clients(world, clients):
    """Sort clients by their demand.
    
    Arguments:
        world -- World structural representation.
        clients -- List of client nodes.
    """

    sorted_clients = []

    for client in clients:
        sorted_clients.append((client, world.nodes[client].demand))
    
    return sorted(sorted_clients, key=lambda x: x[1], reverse=True)


def sort_centers(world, client, centers):
    """Sort centers by their distance to client.
    
    Arguments:
        world -- World structural representation.
        clients -- List of client nodes.
        centers -- List of center(median) nodes.
    """
    
    sorted_centers = []
    for center in centers:
        sorted_centers.append((center, world.distances[client][center]))


    return sorted(sorted_centers, key=lambda x: x[1])