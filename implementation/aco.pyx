#!/usr/bin/env python3

"""ACO(MMAS) methods to solve the capacitated p-medians problem"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import gap
import numpy as np
from solution import Solution


def information_heuristic(world):
    """Information heuristic based in cluster density.
    
    Arguments:
        world -- World structural representation.
    """

    ni = []

    for node in range(len(world.nodes)):
        ordered_nodes = sort_nodes(world, node)
        all_nodes, sum_distance = allocate(world, node, ordered_nodes)
        ni.append(all_nodes / sum_distance)

    return np.array(ni)


def sort_nodes(world, center):
    """Sort all nodes based on their distance to a central node.

    Arguments:
        world -- World structural representation.
        center -- Central node.
    """

    ordered_nodes = []

    for node in range(len(world.nodes)):
        if node != center:
            ordered_nodes.append((node, world.distances[node][center]))
    sorted(ordered_nodes, key=lambda x: x[1])

    return ordered_nodes


def allocate(world, center, ordered_nodes):
    """Assign nodes to a central node until its capacity is fulfilled.

    Arguments:
        world -- World structural representation.
        center -- Central nodes.
        ordered_nodes -- Array of sorted nodes according to their distance to 
                         center.
    """

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
    """Calculate the probability to choose each node from a list of possible
    nodes.
    
    Arguments:
        world -- World structural representation.
        possible_nodes -- List of choosable nodes .
        ni -- Information heuristic vector.
        alpha -- Pheromone exponent in probability calculation.
        beta -- Information Heuristic exponent in probability calculation.
    """

    n = world.n  # Number of nodes
    pheromones = np.array([node.pheromone for node in world.nodes])

    combination = np.multiply(np.power(np.multiply(pheromones, 
                                                   possible_nodes),
                                       alpha),
                              np.power(np.multiply(ni,
                                                   possible_nodes),
                                       beta))
    total_probabilities = np.sum(combination)
    probabilities = np.divide(combination, total_probabilities)

    return probabilities


def evaluate_solutions(world, colony):
    """Evaluate the solutions created by the ants in the colony.
    
    Arguments:
        world -- World structural representation.
        colony -- Colony of ants.
    """

    best = Solution(distance=np.inf)
    worst = Solution(distance=0)

    for ant in colony.ants:
        association = gap.GAP(world, ant)
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


def is_stagnated(world, t_min, t_max):
    """Check if the pheromone levels are stagnating the solution.
    
    Arguments:
        world -- World structural representation.
        t_min -- Min pheromone level.
        t_max -- Max pheromone level.
    """

    total_pheromone = world.total_pheromone()
    stagnation_threshold = world.p * t_max + (world.n - world.p) * t_min

    # Empirical 0.5 threshold to conclude stagnation
    if total_pheromone >= stagnation_threshold - 0.5:
        return True
    else:
        return False
