#!/usr/bin/env python3

"""GAP heuristic to solve the capacitated p-medians problem"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import utils
import numpy as np


def GAP(world, ant):
    n = world.n
    p = world.p
    centers = ant.medians  # Medians
    clients = list(set(np.arange(n)) - set(centers))  # Non-medians
    association = np.zeros((n, n))

    ordered_clients = sort_clients(world, clients, centers)
    for client in ordered_clients:
        ordered_centers = sort_centers(world, client[0], centers)

        for center in ordered_centers:
            capacity = world.nodes[center[0]].actual_capacity

            if capacity - world.nodes[client[0]].demand >= 0:
                capacity -= world.nodes[client[0]].demand
                world.nodes[center[0]].actual_capacity = capacity
                association[client[0]][center[0]] = 1
                break 

    # Reset nodes capacity
    for center in centers:
        world.nodes[center].actual_capacity = world.nodes[center].capacity

    return association


def sort_clients(world, clients, centers):
    sorted_clients = []

    for client in clients:
        sorted_clients.append((client, world.nodes[client].demand))
    
    return sorted(sorted_clients, key=lambda x: x[1], reverse=True)


def sort_centers(world, client, centers):
    sorted_centers = []
    for center in centers:
        sorted_centers.append((center, 
                               utils.euclidean_distance(world.nodes[client], 
                                                        world.nodes[center])))

    return sorted(sorted_centers, key=lambda x: x[1])