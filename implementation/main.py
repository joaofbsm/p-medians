#!/usr/bin/env python3

"""
ACO with heuristics as a solution to the capacitated p-medians problem based in
the paper De França, Fabrício Olivetti, Fernando J. Von Zuben, and Leandro 
Nunes De Castro. "Max min ant system and capacitated p-medians: Extensions and 
improved solutions." Informatica 29.2 (2005).
"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import aco
import math
import utils
import argparse
import numpy as np
from tqdm import tqdm
from node import Node
from world import World
from colony import Colony
from solution import Solution

# TODO
# - Run cProfile
# - Use Cython for speedup


def main(args):
    random_seed = 123456
    initial_pheromone = 0.5
    t_min = 0.001
    t_max = 0.999
    rho = 0.9  # TODO: Find optimal value
    alpha = args.alpha  # TODO: Find optimal value
    beta = args.beta  # TODO: Find optimal value

    np.random.seed(random_seed)
    iterations = args.iterations
    n, p, nodes = utils.read_data(args.dataset, initial_pheromone)
    world = World(n, p, nodes)
    n_ants = (n - p) if args.ants is None else args.ants
    colony = Colony(n_ants)
    ni = aco.information_heuristic(world)

    g_best = Solution(distance=math.inf)

    for i in tqdm(range(iterations)):
        for ant in colony.ants:
            ant.build_solution(world, ni, alpha, beta)

        l_best, l_worst = aco.evaluate_solutions(world, colony)

        world.update_pheromones(rho, g_best, l_best, l_worst)

        if aco.is_stagnated(world, t_min, t_max):
            world.reset_pheromones(initial_pheromone)

        if l_best.distance < g_best.distance:
            g_best = l_best

        colony.reset_solutions()

    print("\nBest solution\n"
          "-------------\n"
          "\n"
          "Distance: {}\n"
          "Medians: {}\n"
          "Association: {}\n".format(g_best.distance, 
                                     g_best.medians,
                                     g_best.association))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("ACO with heuristics to"
                                   " solve the capacitated p-medians problem"))
    parser.add_argument("-i", "--iterations", type=int, default=50)
    parser.add_argument("-a", "--ants", type=int, default=None)
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--beta", type=float, default=0.5)
    parser.add_argument("dataset")
    args = parser.parse_args()

    main(args)