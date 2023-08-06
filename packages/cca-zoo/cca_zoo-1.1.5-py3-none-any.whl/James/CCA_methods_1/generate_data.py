import numpy as np

def generate_data(n, p, q, cors=3):
    X = np.random.rand(n, p)
    Y = np.random.rand(n, q)
    for c in range(cors):
        rand_plus_minus = np.random.randint(0, 1) * 2 - 1
        Y[:, c] = rand_plus_minus * X[:, c] + np.random.rand(n)
    return X, Y




