#!/usr/bin/env python3

"""Node in a bidimensional space"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"


class Node:
    def __init__(self, x, y, capacity, demand, pheromone):
        """Node constructor.
        
        Arguments:
            x -- x axis position.
            y -- y axis position.
            capacity -- Node capacity.
            demand -- Node demand.
            pheromone -- Pheromone level of the node.
        """
        
        self.x = x
        self.y = y
        self.capacity = capacity - demand  # Allocates it's demand to itself
        self.actual_capacity = self.capacity
        self.demand = demand
        self.pheromone = pheromone
