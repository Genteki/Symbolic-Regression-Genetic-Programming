from symbolic_node import *
from params import *
import numpy as np

class GeneticPrograming:
    def __init__(self, params=default_params):
        self.max_degree = params["max_degree"]
        self.pop_size = params["pop_size"]
        self.select_pressure = params["select_pressure"]
        self.pop = []
        self.fitness = np.ones(params["pop_size"])
        self.reproduction_rate = np.array(params["repoduction_rate"], dtype=np.float32)

    def init_population(self):
        self.pop = []
        for i in range(pop_size):
            new_node = SymbolicNode(max_degree=self.max_degree)
            self.pop.append(new_node.random_grow().copy())

    def _cal_fitness(self, x_test, y_test, fitness_function=one_over_mse):
        for i in range(len(self.pop)):
            p = self.pop[i]
            y_predict = p.post_order_traverse_recursive(x_test)
            self.fitness[i] = fitness_function(y_predict, y_test)

    def _tournament(self):
        tournament_size = int(self.select_pressure * self.pop_size)
        candidates = np.random.randint(self.pop_size, size=tournament_size)
        parent = candidates[self.fitness[candidates].argmax()]
        return parent

    def crossover(self):
        pass
