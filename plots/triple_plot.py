import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use("ggplot")

dataset = "SJC1"
iterations = [25, 50, 100]


fig, axes = plt.subplots(nrows=1, ncols=3)

for i, num_gen in enumerate(num_gens):
    axes[i].set_xlabel("Generations")
    axes[i].set_ylabel("Fitness")
    axes[i].set_title("With {} generations".format(num_gen))
    #axes[i].tick_params(labelsize=6)
    for pop_size in pop_sizes:
        all_gen = np.zeros((num_gen + 1, 1))

        for repetition in range(num_repetitions):
            file_name = ("../results/" + dataset + "p" + str(pop_size) + "g" + str(num_gen) + "t" + str(tournament_size) 
                         + "c" + str(crossover_prob) + "m" + str(mutation_prob) + "e" + elitism + "/" + str(repetition + 1) + ".csv")
            content = np.genfromtxt(file_name,  dtype = "float", delimiter = ",")
            content = content[:,1].reshape((num_gen + 1, 1))
            all_gen = np.hstack((all_gen, content))

            #print(file_name)

        all_gen = all_gen[:, 1:]
        avg = np.average(all_gen, axis=1)
        std_dev = np.std(all_gen, axis=1)


        """
        if elitism == "True":
            label = ("popsize = " + str(pop_size) + ", gens = " + str(num_gen) + ", tournsize = " + str(tournament_size)
                    + ", crossprob = " + str(crossover_prob) + ", mutationprob = " + str(mutation_prob) + " with elitism")
        else:
            label = ("popsize = " + str(popsize) + ", gens = " + str(num_gen) + ", tournsize = " + str(tournament_size)
                    + ", crossprob = " + str(crossover_prob) + ", mutationprob = " + str(mutation_prob) + " without elitism")
        """

        label = "Population size = {}".format(pop_size)
        axes[i].plot(np.arange(num_gen + 1), avg, label=label)
        axes[i].fill_between(np.arange(num_gen + 1), avg - std_dev, avg + std_dev, alpha=0.2)
        legend = axes[i].legend(loc='upper right')
        
#plt.suptitle("Keijzer-7 best individual average training fitness")
#plt.suptitle("Keijzer-10 best individual average training fitness")
plt.subplots_adjust(wspace=0.4)

plt.show(block=False)
input("Hit Enter To Close")
plt.close()
