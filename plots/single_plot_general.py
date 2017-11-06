#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")

n_repetitions = 30

datasets = [("SJC1", 100, 10), ("SJC2", 200, 15), ("SJC3b", 300, 30)]

dataset_name, n, p = datasets[0]

n_iterations = [25, 50, 100]
n_ants = n - p
#n_ants = [p, n - p, 2 * (n - p)]
rho = 0.9
#rho = [0.1, 0.5, 0.9]
alpha = 0.5
#alpha = [0.5, 1, 0, 3]
beta = 0.5
#beta = [0.5, 0, 1, 1]

fig, ax = plt.subplots()

ax.set_xlabel("Iterations")
ax.set_ylabel("Total Distance")

for i, iterations in enumerate(n_iterations):
    avg = []
    std_dev = []

    g_best = np.zeros((iterations, 1))
    l_best = np.zeros((iterations, 1))
    l_worst = np.zeros((iterations, 1))
    for repetition in range(n_repetitions):
        file_path = "../results/{}it{}rho{}alpha{}beta{}ants{}/{}.csv".format(
                                                                  dataset_name, 
                                                                  iterations,
                                                                  rho,
                                                                  alpha,
                                                                  beta,
                                                                  n_ants,
                                                                  repetition)

        content = np.genfromtxt(file_path,  dtype = "float", delimiter = ",")
        g_best = np.hstack((g_best, content[:, 1].reshape((iterations, 1))))
        l_best = np.hstack((g_best, content[:, 2].reshape((iterations, 1))))
        l_worst = np.hstack((g_best, content[:, 3].reshape((iterations, 1))))

    g_best = g_best[:, 1:]
    l_best = l_best[:, 1:]
    l_worst = l_worst[:, 1:]

    avg.append(np.average(g_best, axis=1))
    avg.append(np.average(l_best, axis=1))
    avg.append(np.average(l_worst, axis=1))

    std_dev.append(np.std(g_best, axis=1))
    std_dev.append(np.std(l_best, axis=1))
    std_dev.append(np.std(l_worst, axis=1))

    label = "{} iterations - best global".format(iterations)
    ax.plot(np.arange(iterations), avg[0], label=label)
    ax.fill_between(np.arange(iterations), avg[0] - std_dev[0], avg[0] + std_dev[0], alpha=0.2)

    label = "{} iterations - best local".format(iterations)
    ax.plot(np.arange(iterations), avg[1], label=label)
    ax.fill_between(np.arange(iterations), avg[1] - std_dev[1], avg[1] + std_dev[1], alpha=0.2)

    legend = ax.legend(loc='upper right')
        
#plt.subplots_adjust(wspace=0.4)

plt.show(block=False)
input("Hit Enter To Close")
plt.close()
