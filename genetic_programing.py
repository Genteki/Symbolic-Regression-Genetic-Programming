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

    def _roulette(self):
        roulette_size = int(self.select_pressure * self.pop_size)
        candidates = np.random.randint(self.pop_size, size=roulette_size)
        p = self.fitness[candidates] ** 2
        p = p / p.sum()
        parent = np.random.choice(candidates,size=1,p=p)[0]
        return parent

    def _sort_degree(self):
        for tree in pop:
            tree.sort_degree()

    def _cut_off(self, offspring, last_size=10):
        fn = np.ones(len(offspring))
        for i in range(len(offspring)):
            y_predict = offspring[i].post_order_traverse_recursive(self.x_test)
            fn[i] = self.fitness_function(y_predict, self.y_test)
        idx_off = fn.argsort()[::-1][0:self.pop_size-last_size]
        idx_pop = self.fitness.argsort()[::-1][0:last_size]
        new_pop = []
        for i in idx_off:
            new_pop.append(offspring[i].copy())
        for i in idx_pop:
            new_pop.append(self.pop[i].copy())
        self.pop = new_pop
        self.fitness = np.r_[fn[idx_off], self.fitness[idx_pop]]

    def evolve(self):
        offspring = []
        for i in range(self.pop_size):
            parent_i = self._tournament()
            parent = self.pop[parent_i].copy()
            p = np.random.rand()
            if p < self.evo_rate[0]:                # crossover
                parent2 = self.pop[self._tournament()].copy()
                parent2_subtree_idx = parent2.rand_subtree_index()
                parent_subtree_idx = parent.rand_subtree_index()
                parent.all_node[parent_subtree_idx].copy2(parent2.all_node[parent2_subtree_idx])
            elif p < self.evo_rate[0:2].sum():      # subtree mutation
                parent.mutate_subtree()
            elif p < self.evo_rate[0:3].sum():      # point mutation
                parent.mutate_point()
            elif p < self.evo_rate[0:4].sum():      # hoist mutation
                parent.mutate_hoist()
            offspring.append(parent)
        self._cut_off(offspring)
        self._update_best()

    def evolve_roulette(self):
        offspring = []
        for i in range(self.pop_size):
            parent_i = self._roulette()
            parent = self.pop[parent_i].copy()
            p = np.random.rand()
            if p < self.evo_rate[0]:                # crossover
                parent2 = self.pop[self._roulette()].copy()
                parent2_subtree_idx = parent2.rand_subtree_index()
                parent_subtree_idx = parent.rand_subtree_index()
                parent.all_node[parent_subtree_idx].copy2(parent2.all_node[parent2_subtree_idx])
            elif p < self.evo_rate[0:2].sum():      # subtree mutation
                parent.mutate_subtree()
            elif p < self.evo_rate[0:3].sum():      # point mutation
                parent.mutate_point()
            elif p < self.evo_rate[0:4].sum():      # hoist mutation
                parent.mutate_hoist()
            offspring.append(parent)
        self._cut_off(offspring)
        self._update_best()

def test_gp_animate(p=default_params):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style("whitegrid")
    with open("data/data.txt") as ifile:
        lines = ifile.readlines()
        pts = np.array([line.strip().split(",") for line in lines],
                       dtype=np.float32)
    x = pts[:,0]
    y = pts[:,1]
    x_train, y_train, x_test, y_test = split_dataset(x,y,ratio=0.9)
    x_train, y_train, x_test, y_test = x_train.T, y_train.T, x_test.T, y_test.T
    gp = GeneticPrograming(x_train, y_train, one_over_mse, params=p)
    gp.init_population()
    plt.ion();
    plt.figure(figsize=(8,4))
    ax = plt.subplot(1,1,1)
    ax.scatter(x, y, marker=".", color="k",s=1)
    ax.set_ylim(-2,3)
    text = plt.text(1,2,"y=")
    title = plt.title("Best Fitness Function of GA, Tournament Strategy")
    best_fitness = gp.best_fitness
    for i in range(1000):
        gp.evolve()
        y_predict = gp.best_node.post_order_traverse_recursive(y_test)
        test_fit = one_over_mse(y_predict, y_test)
        print(i, gp.best_fitness, test_fit)
        #print(gp.best_node)
        if gp.best_fitness > best_fitness:
            best_fitness = gp.best_fitness
            best_node = gp.best_node
            x_plot = np.linspace(0,20,1000)
            y_plot = gp.best_node.post_order_traverse_recursive(x_plot)
            if type(y_plot)==np.float64: y_plot = np.zeros_like(y) + y_plot
            if len(y_plot) == 1: y_plot = np.zeros_like(y) + y_plot[0]
            ax.lines.clear()
            ax.plot(x_plot, y_plot, color="b")
            text.set_text("y="+str(best_node)+"\nN = "+str(i)); plt.pause(0.05)


if __name__ == '__main__':
    test_gp_animate(p=default_params)
