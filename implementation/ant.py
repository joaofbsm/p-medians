#!/usr/bin/env python3

"""Ant entity"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import aco
import numpy as np
from utils import euclidean_distance


class Ant:
    def __init__(self):
        self.medians = []
    

    def build_solution(self, world, ni, alpha, beta):
        n = world.n
        p = world.p
        unchosen = [*range(n)]

        for median in range(p):
            probabilities = aco.calculate_probabilities(world, unchosen, ni,
                                                        alpha, beta)
            choice = np.random.choice(n, p=probabilities)
            self.medians.append(choice)
            unchosen.remove(choice)


    def reset_solution(self):
        self.medians = []
