from symbolic_node import *
from parameters import *
import numpy as np
np.seterr(divide='ignore')

class GeneticPrograming:
    def __init__(self, x_test, y_test, fitness_function=one_over_mse, params=default_params):
        self.max_degree = params["max_degree"]
        self.pop_size = params["pop_size"]
        self.select_pressure = params["select_pressure"]
        self.pop = []
        self.fitness = np.ones(params["pop_size"])
        self.evo_rate = np.array(params["evo_rate"], dtype=np.float32)
        self.best_fitness = 0
        self.best_node = None
        self.x_test = x_test
        self.y_test = y_test
        self.fitness_function = fitness_function

    def init_population(self):
        self.pop = []
        for i in range(self.pop_size):
            new_node = SymbolicNode(max_degree=self.max_degree)
            self.pop.append(new_node.random_grow().copy())
        self._cal_fitness()
        self.best_fitness = self.fitness.max()
        self.best_node = self.pop[self.fitness.argmax()]

    def _cal_fitness(self, default_vaule=0):
        for i in range(len(self.pop)):
            p = self.pop[i]
            y_predict = p.post_order_traverse_recursive(self.x_test)
            self.fitness[i] = self.fitness_function(y_predict, self.y_test)
        self.fitness[np.isnan(self.fitness)] = default_vaule

    def _update_best(self):
        self._cal_fitness()
        if self.fitness.max() > self.best_fitness:
            self.best_fitness = self.fitness.max()
            self.best_node = self.pop[self.fitness.argmax()]


    def _tournament(self):
        tournament_size = int(self.select_pressure * self.pop_size)
        candidates = np.random.randint(self.pop_size, size=tournament_size)
        parent = candidates[self.fitness[candidates].argmax()]
        return parent

    def _sort_degree(self):
        for tree in pop:
            tree.sort_degree()


    def evolve(self, n_generation=N_GENERATION):
        offspring = []
        for i in range(self.pop_size):
            parent_i = self._tournament()
            parent = self.pop[parent_i].copy()
            p = np.random.rand()
            if p < self.evo_rate[0]:                # crossover
                parent2 = self.pop[self._tournament()].copy()
                parent2_subtree_idx = parent2.rand_subtree_index()
                parent2_subtree = parent2.all_node[parent2_subtree_idx]
                parent_subtree_idx = parent.rand_subtree_index()
                parent_subtree = parent.all_node[parent_subtree_idx]
                parent_subtree.copy2(parent2_subtree)
            elif p < self.evo_rate[0:2].sum():      # subtree mutation
                parent.mutate_subtree()
            elif p < self.evo_rate[0:3].sum():      # point mutation
                parent.mutate_point()
            elif p < self.evo_rate[0:4].sum():      # hoist mutation
                parent.mutate_hoist()
            offspring.append(parent)
        #
        self.pop = offspring
        self._update_best()

def test_gp():
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style("whitegrid")
    with open("data/data.txt") as ifile:
        lines = ifile.readlines()
        pts = np.array([line.strip().split(",") for line in lines],
                       dtype=np.float32)
    x = pts[:,0]
    y = pts[:,1]
    gp = GeneticPrograming(x,y,one_over_mse)
    gp.init_population()
    plt.ion();
    plt.figure(figsize=(8,4))
    ax = plt.subplot(1,1,1)
    ax.scatter(x, y, marker=".", color="k",s=1)
    #ax.set_ylim(-2,2)
    title = plt.title("Best Fitness Function of GP")
    for i in range(N_GENERATION):
        gp.evolve()
        print(i, gp.best_fitness)
        y_predict = gp.best_node.post_order_traverse_recursive(x)
        if y_predict.shape[0]==1: y_predict = np.zeors_like(y) + y_predict[0]
        plt.gca().lines.clear()
        plt.plot(x, y_predict, color="b"); plt.pause(0.05)

if __name__ == '__main__':
    test_gp()
