#!/usr/bin/env python3

"""
ACO as MMAS and GAP heuristic methods to be used for the capacitated p-medians
problem.
"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import math
import utils
import numpy as np
from solution import Solution


def information_heuristic(world):
    ni = []

    for node in range(len(world.nodes)):
        ordered_nodes = sort_nodes(world, node)
        all_nodes, sum_distance = allocate(world, node, ordered_nodes)
        ni.append(all_nodes / sum_distance)

    return ni


def sort_nodes(world, center):
    ordered_nodes = []

    for node in range(len(world.nodes)):
        if node != center:
            ordered_nodes.append((node, world.distances[node][center]))
    sorted(ordered_nodes, key=lambda x: x[1])

    return ordered_nodes


def allocate(world, center, ordered_nodes):
    all_nodes = 0
    sum_distance = 0
    capacity = world.nodes[center].capacity

    for node, distance in ordered_nodes:
        demand = world.nodes[node].demand
        if capacity - demand >= 0:
            all_nodes += 1
            sum_distance += distance
        else:
            break

    return all_nodes, sum_distance


def calculate_probabilities(world, possible_nodes, ni, alpha, beta):
    n = world.n  # Number of nodes

    probabilities = np.zeros(n)
    pheromones = [node.pheromone for node in world.nodes]

    total_probability = 0
    for node in possible_nodes:
        total_probability += ((pheromones[node] ** alpha) *
                              (ni[node] ** beta))

    for node in range(n):
        if node in possible_nodes:
            probabilities[node] = (((pheromones[node] ** alpha) * 
                                    (ni[node] ** beta)) /
                                   total_probability)

    return probabilities


def evaluate_solutions(world, colony):
    best = Solution(distance=math.inf)
    worst = Solution(distance=0)

    for ant in colony.ants:
        association = GAP(world, ant)
        total_distance = np.sum(np.multiply(association, world.distances))
        
        if total_distance < best.distance:
            best.distance = total_distance
            best.medians = ant.medians
            best.association = association
        
        if total_distance > worst.distance:
            worst.distance = total_distance
            worst.medians = ant.medians
            worst.association = association

    return best, worst


def GAP(world, ant):
    n = world.n
    p = world.p
    centers = ant.medians  # Medians
    clients = list(set(np.arange(n)) - set(centers))  # Non-medians
    association = np.zeros((n, n))

    ordered_clients = sort_clients(world, clients, centers)
    for client in ordered_clients:
        ordered_centers = sort_centers(world, client[0], centers)

        attributed = False

        for center in ordered_centers:
            capacity = world.nodes[center[0]].actual_capacity
            if capacity - world.nodes[client[0]].demand >= 0:
                capacity -= world.nodes[client[0]].demand
                world.nodes[center[0]].actual_capacity = capacity
                association[client[0]][center[0]] = 1
                attributed = True
                break 

        if not attributed:
            print("FODEU")
            input()

    # Reset nodes capacity
    for node in world.nodes:
        node.actual_capacity = node.capacity



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


def is_stagnated(world, t_min, t_max):
    total_pheromone = world.total_pheromone()
    stagnation_threshold = world.p * t_max + (world.n - world.p) * t_min


    # Empirical 0.5 threshold to conclude stagnation
    if (total_pheromone <= stagnation_threshold 
        and total_pheromone + 0.5 >= stagnation_threshold):
        return True
    else:
        return False
