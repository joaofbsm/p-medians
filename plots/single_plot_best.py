#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def getColor(c, N, idx):
    import matplotlib as mpl
    cmap = mpl.cm.get_cmap(c)
    norm = mpl.colors.Normalize(vmin=0.0, vmax=N - 1)
    return cmap(norm(idx))

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (16, 10)

n_repetitions = 30

datasets = [("SJC1", 100, 10), ("SJC2", 200, 15), ("SJC3b", 300, 30)]

default_iterations = 50
n_iterations = [25, 50, 100]
default_rho = 0.9
rhos = [0.0, 0.1, 0.5, 0.99]
default_alpha = 0.5
alphas = [1.0, 0.0, 3.0]
default_beta = 0.5
betas = [0.0, 1.0, 1.0]

for dataset_name, n, p in datasets:
    fig, ax = plt.subplots()
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Total Distance")

    default_ants = n - p
    n_ants = [p, 2 * (n - p)]

    datasets_best = {"SJC1": (100, 2 * (n - p), 0.99, 3.0, 1.0), 
                     "SJC2": (100, 2 * (n - p), 0.99, 1.0, 0.0), 
                     "SJC3b": (100, 2 * (n - p), 0.9, 3.0, 1.0)}

    dataset_best_distance = np.inf

    # Iteration plots
    color_index = 0
    for iterations in n_iterations:
        g_best = np.zeros((iterations, 1))
        for repetition in range(n_repetitions):
            file_path = "../results/{}it{}rho{}alpha{}beta{}ants{}/{}.csv".format(
                                                                      dataset_name, 
                                                                      iterations,
                                                                      default_rho,
                                                                      default_alpha,
                                                                      default_beta,
                                                                      default_ants,
                                                                      repetition)

            content = np.genfromtxt(file_path,  dtype = "float", delimiter = ",")
            g_best = np.hstack((g_best, content[:, 1].reshape((iterations, 1))))

        g_best = g_best[:, 1:]
        best = np.amin(g_best, axis=1)

        if best[-1] < dataset_best_distance:
            dataset_best_distance = best[-1]

        label = "{} iterations | {} ants | rho {} | alpha {}, beta {}".format(iterations, default_ants, default_rho, default_alpha, default_beta)
        ax.plot(np.arange(iterations), best, label=label, color=getColor("viridis", len(n_iterations), color_index))
        color_index += 1

    # Ants plots
    color_index = 0
    for ants in n_ants:
        g_best = np.zeros((default_iterations, 1))
        for repetition in range(n_repetitions):
            file_path = "../results/{}it{}rho{}alpha{}beta{}ants{}/{}.csv".format(
                                                                      dataset_name, 
                                                                      default_iterations,
                                                                      default_rho,
                                                                      default_alpha,
                                                                      default_beta,
                                                                      ants,
                                                                      repetition)

            content = np.genfromtxt(file_path,  dtype = "float", delimiter = ",")
            g_best = np.hstack((g_best, content[:, 1].reshape((default_iterations, 1))))

        g_best = g_best[:, 1:]
        best = np.amin(g_best, axis=1)

        if best[-1] < dataset_best_distance:
            dataset_best_distance = best[-1]

        label = "{} iterations | {} ants | rho {} | alpha {}, beta {}".format(default_iterations, ants, default_rho, default_alpha, default_beta)
        ax.plot(np.arange(default_iterations), best, label=label, color=getColor("magma", len(n_ants), color_index))
        color_index += 1

    # Rho plots
    for rho in rhos:
        g_best = np.zeros((default_iterations, 1))
        for repetition in range(n_repetitions):
            file_path = "../results/{}it{}rho{}alpha{}beta{}ants{}/{}.csv".format(
                                                                      dataset_name, 
                                                                      default_iterations,
                                                                      rho,
                                                                      default_alpha,
                                                                      default_beta,
                                                                      default_ants,
                                                                      repetition)

            content = np.genfromtxt(file_path,  dtype = "float", delimiter = ",")
            g_best = np.hstack((g_best, content[:, 1].reshape((default_iterations, 1))))

        g_best = g_best[:, 1:]
        best = np.amin(g_best, axis=1)

        if best[-1] < dataset_best_distance:
            dataset_best_distance = best[-1]

        label = "{} iterations | {} ants | rho {} | alpha {}, beta {}".format(default_iterations, default_ants, rho, default_alpha, default_beta)
        ax.plot(np.arange(default_iterations), best, label=label)

    # Alpha, Beta plots
    for i in range(len(alphas)):
        alpha = alphas[i]
        beta = betas[i]

        g_best = np.zeros((default_iterations, 1))
        for repetition in range(n_repetitions):
            file_path = "../results/{}it{}rho{}alpha{}beta{}ants{}/{}.csv".format(
                                                                      dataset_name, 
                                                                      default_iterations,
                                                                      default_rho,
                                                                      alpha,
                                                                      beta,
                                                                      default_ants,
                                                                      repetition)

            content = np.genfromtxt(file_path,  dtype = "float", delimiter = ",")
            g_best = np.hstack((g_best, content[:, 1].reshape((default_iterations, 1))))

        g_best = g_best[:, 1:]
        best = np.amin(g_best, axis=1)

        if best[-1] < dataset_best_distance:
            dataset_best_distance = best[-1]

        label = "{} iterations | {} ants | rho {} | alpha {}, beta {}".format(default_iterations, default_ants, default_rho, alpha, beta)
        ax.plot(np.arange(default_iterations), best, label=label)

    # Best of all
    iterations, ants, rho, alpha, beta = datasets_best[dataset_name]
    g_best = np.zeros((iterations, 1))
    for repetition in range(n_repetitions):
        file_path = "../results/{}it{}rho{}alpha{}beta{}ants{}/{}.csv".format(
                                                                  dataset_name, 
                                                                  iterations,
                                                                  rho,
                                                                  alpha,
                                                                  beta,
                                                                  ants,
                                                                  repetition)

        content = np.genfromtxt(file_path,  dtype = "float", delimiter = ",")
        g_best = np.hstack((g_best, content[:, 1].reshape((iterations, 1))))

    g_best = g_best[:, 1:]
    best = np.amin(g_best, axis=1)

    if best[-1] < dataset_best_distance:
        dataset_best_distance = best[-1]   

    label = "BEST - {} iterations | {} ants | rho {} | alpha {}, beta {}".format(iterations, ants, rho, alpha, beta)
    ax.plot(np.arange(iterations), best, label=label, color='m')

    print("Best value for {}: {}".format(dataset_name, dataset_best_distance))

    if dataset_name == "SJC1":
        legend = ax.legend(loc='center right')
    elif dataset_name == "SJC3b":
        legend = ax.legend(loc='center left')
    else:
        legend = ax.legend(loc='upper right')

    #plt.show(block=False)
    #input("Hit Enter To Close")
    #plt.close()
    plt.savefig("{}/{}_best.png".format(dataset_name, dataset_name), dpi=200, bbox_inches="tight")
