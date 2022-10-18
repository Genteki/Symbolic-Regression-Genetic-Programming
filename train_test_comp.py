from genetic_programing import *
from utils import *
from parameters import *
import numpy as np
import sys


def test(output_file, p=default_params, N = N_GENERATION ,intvl=1):
    with open("data/data.txt") as ifile:
        lines = ifile.readlines()
        pts = np.array([line.strip().split(",") for line in lines],
                       dtype=np.float32)
    x = pts[:,0]
    y = pts[:,1]
    x_train, y_train, x_test, y_test = split_dataset(x,y,ratio=0.7)
    x_train, y_train, x_test, y_test = x_train.T, y_train.T, x_test.T, y_test.T
    gp = GeneticPrograming(x_train, y_train, one_over_mse, params=p)
    gp.init_population()
    o_file = open("output/"+output_file+".txt", "w")
    for i in range(N):
        gp.evolve()
        y_predict = gp.best_node.post_order_traverse_recursive(x_test)
        test_fit = one_over_mse(y_predict, y_test)
        o_file.write(str(gp.best_fitness)+", "+str(test_fit))
        o_file.write("\n")
        if not (i%intvl):
            print(i, ": ", gp.best_fitness, ",", test_fit)
    o_file.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        N = int(sys.argv[2])
        p = params_list[int(sys.argv[3])]
    else:
        filename = "test"
        N = 2000
        p = gp_tournmant_lowpressure_params
    test(filename,N=N,p=p)
