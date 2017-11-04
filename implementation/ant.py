#!/usr/bin/env python3

"""Ant entity"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import numpy as np
from utils import euclidean_distance


class Ant:
    def __init__(self):
        self.solution = (0, [])  # (total distance, list of nodes)
    

    def build_solution(self, world):
        n = world.n
        p = world.p
        unchosen = [*range(n)]

        for median in range(p):
            #print("Unchosen", unchosen)
            probabilities = world.calculate_probabilities(unchosen)
            #print("Prob", probabilities)
            choice = np.random.choice(n, p=probabilities)
            self.solution[1].append(choice)
            unchosen.remove(choice)


    def GAP(self, world):
        n = world.n
        p = world.p
        centers = self.solution[1]  # Medians
        clients = list(set(np.arange(n)) - set(centers))  # Non-medians
        association = np.zeros((n, n))

        """
        for center in centers:
            association[center][center] = 1
        """

        ordered_clients = self.sort_clients(world, clients, centers)
        for client in ordered_clients:
            ordered_centers = self.sort_centers(world, client[0], centers)
            for center in ordered_centers:
                capacity = world.nodes[center[0]].actual_capacity
                if capacity - world.nodes[client[0]].demand >= 0:
                    capacity -= world.nodes[client[0]].demand
                    association[client[0]][center[0]] = 1
                    break 

        return association


    def sort_clients(self, world, clients, centers):
        sorted_clients = []

        for client in clients:
            distances = []
            for center in centers:
                distances.append(euclidean_distance(world.nodes[client],
                                                    world.nodes[center]))

            sorted_clients.append((client, sorted(distances)[0]))
        
        return sorted(sorted_clients, key=lambda x: x[1])


    def sort_centers(self, world, client, centers):
        sorted_centers = []
        for center in centers:
            sorted_centers.append((center, 
                                   euclidean_distance(world.nodes[client], 
                                                      world.nodes[center])))

        return sorted(sorted_centers, key=lambda x: x[1])


    def reset_solution(self):
        self.solution = (0, [])
