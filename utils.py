import numpy as np

operators = [np.add, np.subtract, np.multiply, np.divide, np.sin, np.cos]
dict_operators = {
    np.add: "+",
    np.subtract: "-",
    np.multiply: "*",
    np.divide: "/",
    np.sin: "sin",
    np.cos: "cos"
}

# generate a random number from -10 to 10
def rand_const():
    r = np.random.rand() * 20 - 10
    if np.abs(r) < 0.0001:
        return rand_const() # regenerate a number if the absolute value is too small to avoid risks
    return r

def rand_operator():
    r = np.random.randint(0,len(operators))
    return operators[r]

#
def split_dataset(X, Y, ratio=0.8):
    X.reshape((X.shape[0],1))
    Y.reshape((Y.shape[0],1))
    data_XY = np.c_[X,Y]
    np.random.shuffle(data_XY)
    train_size = int(data_XY.shape[0] * ratio)
    test_size = data_XY.shape[0] - train_size
    train_X = data_XY[0:train_size, 0:-1]
    train_Y = data_XY[0:train_size, -1]
    test_X = data_XY[train_size:data_XY.shape[0], 0:-1]
    test_Y = data_XY[train_size:data_XY.shape[0], -1]
    return train_X, train_Y, test_X, test_Y

def one_over_mse(A, B):
    return 1 / ((A-B)**2).mean()
