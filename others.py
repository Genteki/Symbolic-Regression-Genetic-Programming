from genetic_programing import *
from utils import *
from parameters import *
import numpy as np
import sys

def others(output_file, N):
    with open("data/data.txt") as ifile:
        lines = ifile.readlines()
        pts = np.array([line.strip().split(",") for line in lines],
                       dtype=np.float32)
    x = pts[:,0]
    y = pts[:,1]
    x_train, y_train, x_test, y_test = split_dataset(x,y,ratio=0.8)
    x_train, y_train, x_test, y_test = x_train.T, y_train.T, x_test.T, y_test.T
    gp = GeneticPrograming(x_train, y_train, one_over_mse, params=params_list[3])
    gp.init_population()

    complexity_file = open("output/"+output_file+"complexity.txt", "w")
    best_complexity_file = open("output/"+output_file+"best_complexity.txt", "w")
    best_fitness_file = open("output/"+output_file+"best_fitness.txt", "w")
    fitness_file = open("output/"+output_file+"fitness.txt", "w")
    convergence_file = open("output/"+output_file+"convergence.txt","w")

    for i in range(N):
        gp.evolve()
        y_predict = gp.best_node.post_order_traverse_recursive(x_test)
        complexity = gp.get_complexity()
        for c in complexity:
            complexity_file.write(str(c) + " ")
        fitness = gp.get_fitness()
        for f in fitness:
            fitness_file.write(str(f) + " ")
        best_complexity = gp.get_best_complexity()
        best_fitness = gp.best_fitness
        best_complexity_file.write(str(best_complexity) + " ")
        best_fitness_file.write(str(best_fitness)+" ")
        convergence_file.write(str(gp.get_convergence_rate())+" ")
        print(i, best_fitness, best_complexity, complexity.max())

    complexity_file.close()
    best_complexity_file.close()
    best_fitness_file.close()
    fitness_file.close()
    convergence_file.close()

if __name__ == '__main__':
    others("others/",2000)
