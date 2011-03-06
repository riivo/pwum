"""
Implemented ideas are from:

Efficient Data Mining for Path Traversal Patterns
Chen, Ming S. and Park, Jong S. and Yu, Philip S.
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.2212
Knowledge and Data Engineering, 1998


Apriori  like implementationn is used instead of originally proposed DHP
"""

from collections import defaultdict

MIN_LEN = 2

def mf(data):
    maximal_forward_refernces  = []
    for session in data:
        sessions = set([])
        mf = [] # current forward refernce
        f  = 1 # direction
        for page in session:
            can_add = -1
            for r in range(len(mf)):
                if mf[r]==page:
                    can_add=r
                    break
                    
            if can_add != -1:
                if f == 1:
                    if len(mf) >= MIN_LEN:
                        sessions.add(tuple([p for p in mf])) # copy
                mf = mf[:r+1]
                f = 0
            else:
                mf.append(page)
                f = 1

            if len(mf) >= MIN_LEN:
                sessions.add(tuple([p for p in mf])) # copy
        
        if len(sessions) > 0:
            maximal_forward_refernces.append(map(lambda x: list(x), sessions))
    
    #stats(maximal_forward_refernces)
    return maximal_forward_refernces
    
 
def large_reference_sequences(data, min_support):
    mfs = mf(data)
    itemsets = extract_itemsets(mfs, min_support)
    some_stats =  prioritize(mfs)
    return itemsets, some_stats


def prioritize(mfs):
    freq_list = defaultdict(lambda: 0)
    
    #transaction contains of multiple independent forward sets
    for trans in mfs:
        trans_set = set([])
        for maximal_forwards in trans:
            trans_set.add(tuple(maximal_forwards))
        
        # only once each item from transaction
        for item in trans_set:
            freq_list[item] += 1
            
    return sorted(freq_list.iteritems(), key=lambda (k,v):(v,k), reverse=True)

# function for finding all frequent items from transactions
def freq_item_count(transactions, min_support):
    freq_item_list = defaultdict(lambda: 0)
    
    #transaction contains of multiple independent forward sets
    for trans in transactions:
        trans_set = set([])
        for maximal_forwards in trans:
            for item in maximal_forwards:
                trans_set.add(item)
        
        # only once each item from transaction
        for item in trans_set:
            freq_item_list[item] += 1
            
    return [x for x in freq_item_list if freq_item_list[x]>=min_support]

# generate itemset_size+1-th candidates from itemset_size-th frequent itemsets
def candidate_gen(k_itemset, itemset_size):
    freq_set_list = []

    for s1 in k_itemset:
        for s2 in k_itemset:
            #generate new itemsets by union of s1 and s2
            if itemset_size == 1:
                candidate = [s1]+[s2]
            else:
                if s1[1:] == s2[:-1]:
                    candidate = [s1[0]] + s2
                else:
                    continue
                    
            #convert candidate set to list
            candidate = [x for x in candidate]
            #only add those itemsets to resulting list that are exactly the size of itemset_size+1
            if len(candidate) == itemset_size+1:
                if candidate not in freq_set_list:
                    freq_set_list+=[candidate]
    #print freq_set_list
    return freq_set_list

# prune the candidates
def prune(transactions, k_itemset, min_support):
    result = []
    for candidate in k_itemset:
        curr_supp = 0
        
        for trans in transactions:
            for maximal_forwards in trans:
                #todo. how to handle support in transactions
                if(is_substring(candidate, maximal_forwards)):
                    curr_supp = curr_supp + 1
                    break

        if curr_supp >= min_support:
            result.append(candidate)
    return result

# extracts all itemsets with support above min_support
def extract_itemsets(transactions, min_support):

    #list of all one element itemsets with support at least equal to min_support
    itemsets = freq_item_count(transactions, min_support)
    itemset_size=0
    rules = []

    while len(itemsets)!=0:
        for item in itemsets:
            if type(item) is not list:
                rules.append([item])
            else:
                rules.append(item)
     
        itemset_size+=1
        
        #generate new candidates
        candidate_set = candidate_gen(itemsets, itemset_size)
        #prune candidates that have less than min_support
        itemsets = prune(transactions, candidate_set, min_support)    
    
    return rules


def is_substring(candidate, maximal_forwards):
    s_mf = ",".join(maximal_forwards)
    s_candidate = ",".join(candidate)
    return s_mf.find(s_candidate) != -1

