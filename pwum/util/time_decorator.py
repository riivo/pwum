'''
a pretty naive approach
'''
import numpy
import operator

def deocarate_timings(patterns, log, total):
    """ return a list of average times spent on each page, based on transaction"""
    transactions = log.sessions
    patterns = sorted(patterns, key=operator.itemgetter(1), reverse=True)
    timings = {}
    for trans in transactions.values():
        if not config.session_filter_fn(trans): continue
        i = 0
        for pattern, support in patterns:
            pos = contains(trans, pattern)
            if pos !=-1:
                timings.setdefault(i, Timing(pattern, support)).sum(pos, trans)
            i+=1

    return timings

 

def output_readable(timings, out):
    out.h1("Sequential patterns with timing ")
    out.tbl()
    for k, v in timings.items():
        v.output(out)
    out.e_tbl()  


def contains(session, pattern):
    """checks where pattern is present in transactions"""
    if len(pattern) == 0: return -1
    i = 0
    j = 0
    
    s = [x.url for x in session]
    for req in s:
        if req == pattern[i]:
            i = i + 1
        else:
            i = 0
        if len(pattern) == i:
            return (j-i)+1
        j+=1  

  
    return -1


class Timing:
    def __init__(self, pattern, support):
        self.pattern = pattern
        self.times = []
        self.support = support
        for _ in self.pattern:
            self.times.append([])
        
    def sum(self, pos, transaction):
        for i in range(0, len(self.times)):
            if pos+i+1 >= len(transaction): return
            delta = transaction[pos+i+1].date - transaction[pos+i].date
            self.times[i].append(delta.seconds)
    
            
    def output(self, out):
        m = [numpy.around(numpy.median(x),2) for x in self.times]
        first = True
        sequence = ""
        for b, a in zip(self.pattern, m):
            if not first:
                sequence +=" -> "
            first = False
            sequence += str(b)+" ("+str(a)+" sec) "
        out.tr([str(round(self.support,2)), sequence])
        
        