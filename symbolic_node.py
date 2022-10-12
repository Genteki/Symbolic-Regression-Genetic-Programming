from utils import *
import numpy as np

class SymbolicNode:
    def __init__(self, degree=0):
        '''

        '''
        self.f = None
        self.lchild = None
        self.rchild = None
        self.n_child = None
        self.value = None
        self.degree = degree

    def post_order_travel_recursive(self, x):
        if self.lchild is None and self.rchild is None:
            if self.value is None:
                return x
            else:
                return self.value
        elif self.rchild is None: # sin, cos
            return self.f(self.lchild.post_order_travel_recursive(x))
        else:
            return self.f(
                self.lchild.post_order_travel_recursive(x),
                self.rchild.post_order_travel_recursive(x) )

    def setNode(self, params):
        self.n_child = len(params) - 1

        if len(params) == 1:        # one number
            if params[0] == "x":    #     x
                return
            else:                   #     a number in [-10, 10]
                self.val = params[0]
        elif len(params) == 2:      # sin, cos
            self.f = params[0]
            self.lchild = params[1]
        elif len(params) == 3:      # add sub mul div
            self.f = params[0]
            self.lchild = params[1]
            self.rchild = params[2]

    def random_grow(self, max_degree=10, stop_rate=0.2, x_rate=0.5):
        if self.degree >= max_degree or np.random.rand() < 0.2:
            if np.random.rand() < x_rate:
                return self
            else:
                self.value = rand_const()
                return self
        else:
            self.f = rand_operator()
            if self.f.nin == 1:
                self.lchild = SymbolicNode(degree=self.degree+1)
                self.lchild.random_grow()
            elif self.f.nin == 2:
                self.lchild = SymbolicNode(degree=self.degree+1)
                self.rchild = SymbolicNode(degree=self.degree+1)
                self.lchild.random_grow()
                self.rchild.random_grow()

    def copy(self):
        new_node = SymbolicNode(degree=self.degree)
        new_node.f = self.f
        new_node.value = self.value
        new_node.n_child = self.n_child
        new_node.value = self.value
        if not self.lchild is None:
            new_node.lchild = self.lchild.copy()
        if not self.rchild is None:
            new_node.rchild = self.rchild.copy()
        return new_node

    def __str__(self):
        if self.f is None:
            if self.value == None:
                return "x"
            else:
                return str(self.value)
        elif self.f.nin == 1:
            return dict_operators[self.f] + "(" + self.lchild.__str__() + ")"
        else:
            return ("(" + str(self.lchild) + dict_operators[self.f] + str(self.rchild) + ")")


def test_rand():
    root = SymbolicNode()
    root.random_grow()
    print(root)

def test_travel():
    root = SymbolicNode()
    l = SymbolicNode(1)
    r = SymbolicNode(1)
    ll = SymbolicNode(1)
    ll = SymbolicNode(1)
    root.setNode([operators[2], l, r])
    l.setNode([operators[0], ll, ll])
    print(root)
    print(root.post_order_travel_recursive(10))

if __name__ == '__main__':
    test_travel()
