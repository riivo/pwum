"""
Various string similarity functions
"""

def jaccard_distance(first, second):
    """
    returns jaccard distance between two strings
    string are converted into sets and each character in string is treated as element in a set
    """
    s1 = set(first)
    s2 = set(second)
    d = len(s1.intersection(s2)) / (len(s1.union(s2)) + 0.0)
    return 1.0 - d
 
def levenshtein(first, second):
    """
    Find the Levenshtein (or edit) distance between two strings.
    """
    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    
    first_length = len(first) + 1
    second_length = len(second) + 1
    
    distance_matrix = [range(second_length) for x in range(first_length)]
    
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i - 1][j] + 1
            insertion = distance_matrix[i][j - 1] + 1
            substitution = distance_matrix[i - 1][j - 1]
            if first[i - 1] != second[j - 1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    
    return distance_matrix[first_length - 1][second_length - 1]

