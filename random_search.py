import sys
import numpy as np
from symbolic_node import *
from utils import *
from genetic_programing import *

def random_search(output_file, N=200 ,max_degree=8, fit=one_over_mse):
    with open("data/data.txt") as ifile:
        lines = ifile.readlines()
        pts = np.array([line.strip().split(",") for line in lines],
                       dtype=np.float32)
    x = pts[:,0]
    y = pts[:,1]

    o_file = open("output/"+output_file+".txt", "w")
    best_fitness = 0.0001
    for i in range(int(N*1000)):
        root = SymbolicNode()
        root.random_grow()
        y_predict = root.post_order_traverse_recursive(x)
        fitness = fit(y_predict, y)
        if best_fitness < fitness:
            best_fitness = fitness
        if not i % 200:
            o_file.write(str(best_fitness)+"\n")
    return

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        N = int(sys.argv[2])
    else:
        filename = "test"
        N = 20
    random_search(filename, N=N)
