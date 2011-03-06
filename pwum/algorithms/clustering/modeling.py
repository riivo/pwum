"""methods for modeling web sessions"""
import numpy as np

def get_markov_model(sessions):
    """
    builds a markov model out of list of sessions
    """
    model = np.zeros(sessions[0].shape, np.float)
    for s in sessions:
        model = model + s
    return normalize(model)
    
        

def normalize(mymatrix):
    """
    nomralizes model, all rows sum up to 1
    """
    
    numrows,numcols=mymatrix.shape
    for i in range(numrows):
        temp = mymatrix[i].sum()
        for j in range(numcols):
            mymatrix[i,j]=abs(mymatrix[i,j]/temp)
    return mymatrix


def convert_sessions_to_vector(sessions, code_book, binary=True):
    """
    convert sessions into feature vectors based on codebook encoding
    session is list of pages
    :binary if True, use 0/1 representation, otherwise number of times page was accessed in sesssion
    """
    models = []
    for session in sessions:
        v1 = np.zeros(len(code_book.keys()), np.int)
        for p in session:
            if p not in code_book:
                continue
            key = code_book[p]
            if binary:
                v1[key] =  1
            else:
                v1[key] +=1
        models.append(v1)
    return models


def convert_sessions_to_markov(sessions, code_book, bayes=True,prior_v=1.0, prior_e = 0.0):
    """
    conver sessions into markov models, e.g estimation first order transtion matrix
    session is list of pages
    """
    models = []
    for session in sessions:
        model = calcualte_transition_matrix(session, code_book, bayes,prior_v, prior_e)
        models.append(model.ravel())
    return models


def calcualte_transition_matrix(session, code_book, bayes_estimation=True, prior_v=1.0, prior_e = 0.0):
    
    """
    esimation transition matrix from session
    bayes estimation uses prior information and makes all transition possible(with small probability)
    """
    size = len(code_book.items())
    
    model = np.zeros((size, size), np.float)
    prev = None
    for page in session:
        #TODO: makes no sense to skip pages
        if page not in code_book:
            continue        
        x = code_book[page]
        if prev == None:
            prev = x
            continue
        model[prev][x] += 1
        prev = x

    #normalize
    x = 0
    for x in range(size):
        sumx = np.sum(model[x])
        if abs(sumx - 0) < 0.00001:
            continue 
        for y in range(len(model)):
            if bayes_estimation is False:
                #well, kind a maximum likelihood
                model[x][y] /= sumx
            else:
                #some prior information, no transition with zero probability
                prior_e = 1.0 * len([c1 for c1 in model[x] if c1 > 0.00001]) 
                model[x][y] = (model[x][y] + prior_e) / ( sumx + prior_v)         
                
    return model 

