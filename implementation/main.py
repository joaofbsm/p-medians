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
import utils
import argparse
import numpy as np
from tqdm import tqdm
from world import World
from colony import Colony
from solution import Solution


def main(args):
    # Parameters
    initial_seed = 123456  # Used to generate the set of seeds for repetitions
    n_repetitions = 30
    n_iterations = args.iterations
    initial_pheromone = 0.5
    t_min = 0.001  # Min pheromone level
    t_max = 0.999  # Max pheromone level
    rho = args.rho  # Pheromone decay rate
    alpha = args.alpha  
    beta = args.beta  

    # Initializations
    random_seeds = utils.generate_seeds(initial_seed, n_repetitions)
    n, p, nodes = utils.read_data(args.dataset)
    world = World(n, p, nodes)
    n_ants = (n - p) if args.ants is None else args.ants
    colony = Colony(n_ants)
    ni = aco.information_heuristic(world)  # Information Heuristic
    dataset_name = args.dataset.split('/')[-1].split('.')[0]
    output = np.zeros((n_repetitions, n_iterations, 3))
    output_dir = "../results/{}it{}rho{}alpha{}beta{}ants{}/".format(
                                                                  dataset_name, 
                                                                  n_iterations,
                                                                  rho,
                                                                  alpha,
                                                                  beta,
                                                                  n_ants)

    # Main loop
    for repetition in range(n_repetitions):
        np.random.seed(random_seeds[repetition])

        # Reset things for new repetition
        g_best = Solution(distance=np.inf)
        world.reset_pheromones(initial_pheromone)

        print("Repetition {}\n".format(repetition))

        for iteration in tqdm(range(n_iterations)):
            for ant in colony.ants:
                ant.build_solution(world, ni, alpha, beta)

            l_best, l_worst = aco.evaluate_solutions(world, colony)

            world.update_pheromones(rho, g_best, l_best, l_worst)

            # Check algorithm stagnation
            if aco.is_stagnated(world, t_min, t_max):
                world.reset_pheromones(initial_pheromone)

            # Update global solution
            if l_best.distance < g_best.distance:
                g_best = l_best

            # Reset for next iteration
            colony.reset_solutions()

            # Store output data
            output[repetition][iteration][0] = g_best.distance
            output[repetition][iteration][1] = l_best.distance
            output[repetition][iteration][2] = l_worst.distance

        print("\nBest solution\n"
              "-------------\n"
              "Distance: {}\n"
              "Medians: {}\n".format(g_best.distance, 
                                     g_best.medians))

    utils.write_data(output_dir, output)


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description=("ACO with heuristics to "
                                    "solve the capacitated p-medians problem"))
    parser.add_argument("-i", "--iterations", type=int, default=50)
    parser.add_argument("-a", "--ants", type=int, default=None)
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--beta", type=float, default=0.5)
    parser.add_argument("--rho", type=float, default=0.9)
    parser.add_argument("dataset")
    args = parser.parse_args()

    main(args)