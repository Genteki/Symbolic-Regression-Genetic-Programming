from genetic_programing import *
from utils import *
from parameters import *
import numpy as np
import sys

def test_gp_tournmant(output_file, p=default_params, N = N_GENERATION ,intvl=10):
    with open("data/data.txt") as ifile:
        lines = ifile.readlines()
        pts = np.array([line.strip().split(",") for line in lines],
                       dtype=np.float32)
    x = pts[:,0]
    y = pts[:,1]
    x_train, y_train, x_test, y_test = split_dataset(x,y,ratio=0.8)
    gp = GeneticPrograming(x, y, one_over_mse, params=p)
    gp.init_population()
    o_file = open("output/"+output_file+".txt", "w")
    express = open("output/"+output_file+"_symbolic.txt", "w")
    for i in range(N):
        gp.evolve()
        o_file.write(str(gp.best_fitness))
        o_file.write("\n")
        if not (i%intvl):
            print(i, ": ", gp.best_fitness)
    o_file.close()
    express.write(str(gp.best_node))
    express.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        N = int(sys.argv[2])
        p = params_list[int(sys.argv[3])]
    else:
        filename = "test"
        N = 20
        p = default_params
    test_gp_tournmant(filename,N=N,p=p)
