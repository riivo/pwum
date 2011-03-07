"""k-mean clustering implementation, should work on any set of feature vectors"""
import numpy as np
from random import choice

def choose_initial(data, k, distfun):
    set_c = []
    while len(set_c) < k:
        choi = choice(data)
        set_c.append(choi)
    return set_c

def eucledian_distance(model1, model2):
    """
    eucledian between two transition matrices
    """
    d = np.abs(model1 - model2)**2
    s = np.sqrt(np.sum(d))
    return s    
def kcluster(data, k, distfun=eucledian_distance, initial=None, t=0.0001,  maxiter=10):
    DOUBLE_MAX = 1.797693e308
    n = len(data)
    shape = data[0].shape
    counts = [0] * k # size of each cluster
    labels = [0] * n # output cluster label for each data point

    c1 = []
    for i in xrange(k):
        c1.append(np.zeros(shape))

    c = choose_initial(data, k, distfun)
    niter = 0   
    error = 0.0

    while True:
        old_error = error
        error = 0.0

        for i in xrange(k):
            counts[i] = 0
            c1[i] = np.zeros(shape)

        for h in xrange(n):
            min_distance = DOUBLE_MAX
            for i in xrange(k):
            
                distance = distfun(data[h],c[i])
                if distance < min_distance:
                    labels[h] = i
                    min_distance = distance

            
            c1[labels[h]] = c1[labels[h]]  + data[h]
            counts[labels[h]] += 1
            error += min_distance


        for i in xrange(k): 
            if counts[i]:
                c[i] = c1[i] / counts[i] 


        niter += 1

        #if verbose: print "%d) Error:" % niter, abs(error - old_error)
        if (abs(error - old_error) < t) or (niter > maxiter):
            break

    return labels, c, error
