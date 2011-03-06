def freq_item_count(transactions, min_support):
    """function for finding all frequent 1-items from transactions"""
    freq_item_list = {}

    for trans in transactions:
        for item in set(trans):
            if item in freq_item_list:
                freq_item_list[item] += 1
            else:
                freq_item_list[item] = 1
    sets = []
    support_db = {}
    
    for x in freq_item_list:
        if freq_item_list[x] >= min_support:
            sets.append(x)
            support_db[tuple(x)] = freq_item_list[x]

    return sorted(sets), support_db




def get_subs(itemset):
    """ return all direct ubsets of a set of length k(i.e. returs subset of k-1) """
    return [itemset[:i] + itemset[i + 1:] for i in range(len(itemset) - 1)]


def candidate_gen(k_itemset, itemset_size):
    """generate candidates of size k+1 based on size k frequent set""" 
    output = []
    #generate by joining
    for fi, first in enumerate(k_itemset[:-1]):
        for _, second in enumerate(k_itemset[fi + 1:]):
            if first[:itemset_size - 2] == second[:itemset_size - 2]:
                new = first + [second[-1]]
                output.append(new)
    
    #prune based on apriori principles: all subsets must be frequent            
    for i, candidate in enumerate(output):
        ok = True
        for candidate_sub in get_subs(candidate):
            if candidate_sub not in k_itemset:
                ok = False
        if not ok:
            del output[i]           
    
    return output

def candidate_gen_l2(sets):
    """Simple candidate generation  for k=2"""
    result = []
    nsets = len(sets)
    for i in range(nsets):
        elt_i = sets[i]
        for j in range(i + 1, len(sets)):
            elt_j = sets[j]
            assert(elt_i < elt_j)
            result.append([elt_i, elt_j])
    return result

def prune(transactions, k_itemset, min_support):
    """prune candidates by checking support in database"""
    
    hold = []
    supports = {}
    for candidate in k_itemset:
        candidate_support = len([trans for trans in transactions if set(candidate) <= set(trans)])
        
        if candidate_support >= min_support:
            supports.setdefault(tuple(candidate), candidate_support)
            hold.append(candidate)
    return hold, supports


def apriori(transactions, min_support):
    """extracts all itemsets with support above min_support"""
    #list of all one element itemsets with support at least equal to min_support
    itemsets, support_db = freq_item_count(transactions, min_support)
    itemset_size = 1
    rules = []
    supports = {}

    
    while len(itemsets) != 0:
        for item in itemsets:
            add = item
            if type(item) is not list: add = [item]
            supports[tuple(add)] = support_db[tuple(item)]
            rules.append(add)
        
        #generate new candidates
        if itemset_size == 1:
            candidate_set = candidate_gen_l2(itemsets)
        else:
            candidate_set = candidate_gen(itemsets, itemset_size + 1)
        
        #prune candidates that have less than min_support
        itemsets, support_db = prune(transactions, candidate_set, min_support)    
        itemset_size += 1
        
    return rules, supports
 
 


