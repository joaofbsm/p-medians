#!/usr/bin/env python3

"""ACO with heuristics as a solution to the capacitated p-medians problem"""

__author__ = "João Francisco Barreto da Silva Martins"
__email__ = "joaofbsm@dcc.ufmg.br"
__license__ = "GPL"
__version__ = "3.0"

import math
import argparse
import numpy as np
from tqdm import tqdm
from node import Node
from world import World
from colony import Colony

# TODO
# - Remove unnecessary attributes from World
# - Use Cython for speedup
# - Update format of solution in ant

def read_data(file_path, initial_pheromone):
    nodes = []

    with open(file_path, 'r') as f:
        n, p = tuple(map(int, f.readline().split()))

        for line in f:
            line = line.split()
            x = int(line[0])
            y = int(line[1])
            capacity = int(line[2])
            demand = int(line[3])
            node = Node(x, y, capacity, demand, initial_pheromone)
            nodes.append(node)

    return n, p, nodes


def main(args):
    random_seed = 123456
    initial_pheromone = 0.5
    t_min = 0.001
    t_max = 0.999
    rho = 0.9  # TODO: Find optimal value

    np.random.seed(random_seed)

    iterations = args.iterations
    n, p, nodes = read_data(args.dataset, initial_pheromone)
    world = World(n, p, nodes, args.alpha, args.beta, t_min, t_max)
    ants = (n - p) if args.ants is None else args.ants
    colony = Colony(ants)

    g_best = (math.inf, [])

    for i in tqdm(range(iterations)):
        for ant in colony.ants:
            ant.build_solution(world)

        l_best, l_worst = world.evaluate_solutions(colony)

        if world.is_stagnated():
            world.reset_pheromones(initial_pheromone)
        else:
            world.update_pheromones(rho, g_best, l_best, l_worst)

        if l_best[0] < g_best[0]:
            g_best = l_best

        colony.reset_solutions()

    print("\nBest solution\n"
          "-------------\n"
          "\n"
          "Distance: {}\n"
          "Medians: {}\n".format(g_best[0], g_best[1]))


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