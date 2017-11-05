#!/usr/bin/env python3

"""World structural representation in p-medians problem"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import math
import utils
import numpy as np
from solution import Solution


class World:
    def __init__(self, n, p, nodes):
        """World constructor.
        
        Arguments:
            n -- Number of nodes.
            p -- Number of medians.
            nodes -- Array of Node objects.
        """

        self.n = n
        self.p = p
        self.nodes = nodes
        self.distances = self.calculate_distances()


    def calculate_distances(self):
        """Calculate distance between nodes and save it to a matrix."""

        distances = np.zeros((self.n, self.n))

        for i, node_i in enumerate(self.nodes):
            for j, node_j in enumerate(self.nodes):
                distances[i][j] = utils.euclidean_distance(node_i, node_j)

        return distances


    def update_pheromones(self, rho, g_best, l_best, l_worst):
        """Update pheromones according to the MMAS rule.
        
        Arguments:
            rho -- Pheromone decay rate.
            g_best -- Global best solution.
            l_best -- Local best solution.
            l_worst -- Local worst solution.
        """

        pheromones = [node.pheromone for node in self.nodes]
        delta_t = self.calculate_delta_t(g_best, l_best, l_worst)

        for i, node in enumerate(self.nodes):
            node.pheromone = (node.pheromone + 
                              (rho * (delta_t[i] - node.pheromone)))


    def calculate_delta_t(self, g_best, l_best, l_worst):
        """Calculate the pheromone deltas.
        
        The deltas are used in the pheromone update formula.
        
        Arguments:
            g_best -- Global best solution.
            l_best -- Local best solution.
            l_worst -- Local worst solution.
        """

        delta_t = np.zeros(len(self.nodes))

        delta = 1 - ((l_best.distance - g_best.distance) / 
                     (l_worst.distance - l_best.distance))
        present_nodes = list(set(g_best.medians) & set(l_best.medians))

        for node in present_nodes:
            delta_t[node] = delta 

        return delta_t


    def total_pheromone(self):
        """Calculate the total pheromone in the world."""

        return sum([node.pheromone for node in self.nodes])


    def reset_pheromones(self, initial_pheromone):
        """Reset the pheromones to the initial level.
        
        Arguments:
            initial_pheromone -- Initial pheromone level.
        """
        
        for node in self.nodes:
            node.pheromone = initial_pheromone
