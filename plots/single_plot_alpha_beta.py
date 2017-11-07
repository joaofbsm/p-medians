#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (16, 10)

n_repetitions = 30

datasets = [("SJC1", 100, 10), ("SJC2", 200, 15), ("SJC3b", 300, 30)]

n_iterations = 50
rho = 0.9
alphas = [0.5, 1.0, 0.0, 3.0]
betas = [0.5, 0.0, 1.0, 1.0]

for dataset_name, n, p in datasets:
    fig, ax = plt.subplots()
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Total Distance")

    n_ants = n - p

    for i in range(len(alphas)):
        alpha = alphas[i]
        beta = betas[i]

        avg = []
        std_dev = []

        g_best = np.zeros((n_iterations, 1))
        l_best = np.zeros((n_iterations, 1))
        l_worst = np.zeros((n_iterations, 1))
        for repetition in range(n_repetitions):
            file_path = "../results/{}it{}rho{}alpha{}beta{}ants{}/{}.csv".format(
                                                                      dataset_name, 
                                                                      n_iterations,
                                                                      rho,
                                                                      alpha,
                                                                      beta,
                                                                      n_ants,
                                                                      repetition)

            content = np.genfromtxt(file_path,  dtype = "float", delimiter = ",")
            g_best = np.hstack((g_best, content[:, 1].reshape((n_iterations, 1))))
            l_best = np.hstack((g_best, content[:, 2].reshape((n_iterations, 1))))
            l_worst = np.hstack((g_best, content[:, 3].reshape((n_iterations, 1))))

        g_best = g_best[:, 1:]
        l_best = l_best[:, 1:]
        l_worst = l_worst[:, 1:]

        avg.append(np.average(g_best, axis=1))
        avg.append(np.average(l_best, axis=1))
        avg.append(np.average(l_worst, axis=1))

        std_dev.append(np.std(g_best, axis=1))
        std_dev.append(np.std(l_best, axis=1))
        std_dev.append(np.std(l_worst, axis=1))

        label = "alpha {}, beta {} - global".format(alpha, beta)
        ax.plot(np.arange(n_iterations), avg[0], label=label)
        ax.fill_between(np.arange(n_iterations), avg[0] - std_dev[0], avg[0] + std_dev[0], alpha=0.2)

        label = "alpha {}, beta {} - local".format(alpha, beta)
        if(i == len(alphas) - 1):
            ax.plot(np.arange(n_iterations), avg[1], label=label, color='m')
        else:
            ax.plot(np.arange(n_iterations), avg[1], label=label)    
        ax.fill_between(np.arange(n_iterations), avg[1] - std_dev[1], avg[1] + std_dev[1], alpha=0.2)

        legend = ax.legend(loc='upper right')

    #plt.show(block=False)
    #input("Hit Enter To Close")
    #plt.close()
    plt.savefig("{}/{}_alpha_beta.png".format(dataset_name, dataset_name), dpi=200, bbox_inches="tight")
