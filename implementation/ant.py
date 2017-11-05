#!/usr/bin/env python3

"""Ant entity"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import aco
import numpy as np


class Ant:
    def __init__(self):
        """Ant constructor."""

        self.medians = []  # Medians on the built solution
    

    def build_solution(self, world, ni, alpha, beta):
        """Choose p-medians with ACO.
        
        Arguments:
            world -- World structural representation
            ni -- Information heuristic vector.
            alpha -- Pheromone exponent in probability calculation.
            beta -- Information Heuristic exponent in probability calculation.
        """

        n = world.n
        p = world.p
        unchosen = np.ones(n)

        for median in range(p):
            probabilities = aco.calculate_probabilities(world, unchosen, ni,
                                                        alpha, beta)
            choice = np.random.choice(n, p=probabilities)
            # Add the chosen median to the solution
            self.medians.append(choice)
            # Remove the chosen node from the possible nodes
            unchosen[choice] = 0  


    def reset_solution(self):
        """Reset ant solution."""
        
        self.medians = []
