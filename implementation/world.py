#!/usr/bin/env python3

"""World structural representation in p-medians problem"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import math
import utils
import numpy as np


class World:
    def __init__(self, n, p, nodes, alpha, beta, t_min, t_max):
        self.n = n
        self.p = p
        self.nodes = nodes
        self.alpha = alpha
        self.beta = beta
        self.t_min = t_min
        self.t_max = t_max

        self.distances = self.calculate_distances()
        self.ni = self.information_heuristic()


    def calculate_distances(self):
        distances = np.zeros((self.n, self.n))

        for i, node_i in enumerate(self.nodes):
            for j, node_j in enumerate(self.nodes):
                distances[i][j] = utils.euclidean_distance(node_i, node_j)

        return distances


    def information_heuristic(self):
        ni = []

        for node in range(len(self.nodes)):
            ordered_nodes = self.sort_nodes(node)
            all_nodes, sum_distance = self.allocate(node, ordered_nodes)
            ni.append(all_nodes / sum_distance)

        return ni


    def sort_nodes(self, center):
        ordered_nodes = []

        for node in range(len(self.nodes)):
            if node != center:
                ordered_nodes.append((node, self.distances[node][center]))
        sorted(ordered_nodes, key=lambda x: x[1])

        return ordered_nodes


    def allocate(self, center, ordered_nodes):
        all_nodes = 0
        sum_distance = 0
        capacity = self.nodes[center].capacity

        for node, distance in ordered_nodes:
            demand = self.nodes[node].demand
            if capacity - demand >= 0:
                all_nodes += 1
                sum_distance += distance
            else:
                break

        return all_nodes, sum_distance


    def calculate_probabilities(self, possible_nodes):
        probabilities = np.zeros(len(self.nodes))
        pheromones = [node.pheromone for node in self.nodes]

        total_probability = 0
        for node in possible_nodes:
            total_probability += ((pheromones[node] ** self.alpha) *
                                  (self.ni[node] ** self.beta))

        for node in range(len(self.nodes)):
            if node in possible_nodes:
                probabilities[node] = (((pheromones[node] ** self.alpha) * 
                                        (self.ni[node] ** self.beta)) /
                                       total_probability)

        return probabilities
    

    def evaluate_solutions(self, colony):
        best_solution = []
        best_distance = math.inf
        worst_solution = []
        worst_distance = 0

        for ant in colony.ants:
            association = ant.GAP(self)
            total_distance = np.sum(np.multiply(association, self.distances))
            
            if total_distance < best_distance:
                best_distance = total_distance
                best_solution = ant.solution[1]
            
            if total_distance > worst_distance:
                worst_distance = total_distance
                worst_solution = ant.solution[1]

            #print(total_distance, ant.solution[1])
            #input()

        return (best_distance, best_solution), (worst_distance, worst_solution)


    def update_pheromones(self, rho, g_best, l_best, l_worst):
        pheromones = [node.pheromone for node in self.nodes]
        print("Pheromones", pheromones)
        delta_t = self.calculate_delta_t(g_best, l_best, l_worst)

        print("Delta", delta_t)

        print("G:", g_best)
        print("LB:", l_best)
        print("LW:", l_worst)

        for i, node in enumerate(self.nodes):
            node.pheromone = (node.pheromone + 
                              (rho * (delta_t[i] - node.pheromone)))


    def calculate_delta_t(self, g_best, l_best, l_worst):
        delta_t = np.zeros(len(self.nodes))

        delta = 1 - ((l_best[0] - g_best[0]) / (l_worst[0] - l_best[0]))
        present_nodes = list(set(g_best[1]) & set(l_best[1]))

        for node in present_nodes:
            delta_t[node] = delta 

        return delta_t


    def is_stagnated(self):
        total_pheromone = self.total_pheromone()
        threshold = self.p * self.t_max + (self.n - self.p) * self.t_min

        print("Total:", total_pheromone)
        print("Threshold:", threshold)

        if total_pheromone <= threshold and total_pheromone + 0.5 >= threshold:
            return True
        else:
            return False


    def total_pheromone(self):
        return sum([node.pheromone for node in self.nodes])


    def reset_pheromones(self, initial_pheromone):
        for node in self.nodes:
            node.pheromone = initial_pheromone
