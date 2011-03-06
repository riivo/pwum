
import numpy
import matplotlib.pyplot as plt
from numpy import dot, linalg, sqrt

def viz(models, filename="last.pdf"):

    fig = plt.figure()
    plt.cla()
    plt.clf()
    ax = fig.add_subplot(111)
    signals, variance, mean = pca(numpy.array(models))
    ax.scatter(signals[:, 0], signals[:, 1])
    
    ax.set_xlabel("First principal component")
    ax.set_ylabel("Second principal component")
    #plt.show()
    plt.savefig(filename)



def pca_int(X):
    # Principal Component Analysis
    # input: X, matrix with training data as flattened arrays in rows
    # return: projection matrix (with important dimensions first),
    # variance and mean
    num_data, dim = X.shape

    #center data
    mean_X = X.mean(axis=0)
    for i in range(num_data):
        X[i] -= mean_X

    M = dot(X, X.T) #covariance matrix
    e, EV = linalg.eigh(M) #eigenvalues and eigenvectors
    tmp = dot(X.T, EV).T 
    V = tmp[:: - 1] #reverse since last eigenvectors are the ones we want
    S = sqrt(e)[:: - 1] #reverse since eigenvalues are in increasing order

    return V, S, mean_X

def pca(X):
    V, S, mean_X = pca_int(X)
    signals = dot(V, X.T).T
    return signals, S, mean_X
