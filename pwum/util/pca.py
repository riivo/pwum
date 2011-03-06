import numpy
import matplotlib.pyplot as plt

def viz(models, filename="last.pdf"):

    fig = plt.figure()
    plt.cla()
    plt.clf()
    ax = fig.add_subplot(111)
    signals, _, _ = pca(numpy.array(models))
    ax.scatter(signals[:, 0], signals[:, 1])
    
    ax.set_xlabel("First principal component")
    ax.set_ylabel("Second principal component")

    plt.savefig(filename)



def pca(X):
    num_data, dim = X.shape

    mean_X = X.mean(axis=0)
    for i in range(num_data):
        X[i] -= mean_X

    M = numpy.dot(X, X.T) #covariance matrix
    e, EV = numpy.linalg.eigh(M) #eigenvalues and eigenvectors
    tmp = numpy.dot(X.T, EV).T 
    V = tmp[:: - 1] #reverse 
    S = numpy.sqrt(e)[:: - 1] #reverse since eigenvalues are in increasing order

    signals = numpy.dot(V, X.T).T
    
    return signals, S, mean_X

