import numpy

class ClusterEval:
    """
    Set of evaluation methods for evalating goodness of clustering
    For more infomation on the measures, refer to any data mining book of your choie
    """
    
    def __init__(self, distance, assignments, elements, type=None, labels=[]):
        self.distance = distance
        self.assignments = assignments
        self.elements = elements
        self.clusters = set(assignments)
        self.labels = labels
        self.label_count = len(set(labels))
        self.type = type

    def entropy(self):
        """
        entropy of clustering
        """
        entropies =[]
        weights = []
        p = numpy.zeros((len(self.clusters), self.label_count), numpy.float)
        m = len(self.assignments) 
        for i in self.clusters:
            mi = 0
            for xi in self.assignments: 
                if xi == i: mi = mi +1
                     
            mj = numpy.zeros((self.label_count), numpy.float)
            for i_new in range(m):
                if self.assignments[i_new] == i:
                    mj[self.labels[i_new]] += 1
            mj = mj / mi
            ei = 0.0
            for j in mj:
                if numpy.abs(j) < 0.0001:
                    continue
                ei += j*numpy.log2(j)
            ei = ei * -1.0
            entropies.append(ei)
            weights.append(mi/(m*1.0))

        return numpy.sum(numpy.array(entropies)*numpy.array(weights))
            
    def purity(self):
        """
        purity, to which degree clusters contain only single class labels
        """
        pure =[]
        weights = []
        p = numpy.zeros((len(self.clusters), self.label_count), numpy.float)
        m = len(self.assignments) 
        for i in self.clusters:
            mi = 0
            for xi in self.assignments: 
                if xi == i: mi = mi +1
                     
            mj = numpy.zeros((self.label_count), numpy.float)
            for i_new in range(m):
                if self.assignments[i_new] == i:
                    mj[self.labels[i_new]] += 1
            mj = mj / mi
            ei = 0.0
            ei = numpy.max(mj)
            pure.append(ei)
            weights.append(mi/(m*1.0))

        return numpy.sum(numpy.array(pure)*numpy.array(weights))        
    
    def sse(self):
        """
        sum of squared errors
        """
        n = len(self.elements)
        sum = 0.0
        for i in self.clusters:
            for x in range(n):
                cluster = self.assignments[x]
                if i == cluster and x != i:
                    sum += self.distance[i][x]**2
        return sum
    
    def silhouette(self):
        """
        slihouette score for clustering
        """
        n = len(self.elements)
        points = [0 for i in range(n)]
        for i in range(n):
            cluster = self.assignments[i]
            asum = []
            bcluster = {}
            for j in range(n):
                if cluster == self.assignments[j] and i != j:
                    try:
                        asum.append(self.distance[i][j])
                    except TypeError:
                        asum.append(self.distance(self.elements[i], self.elements[j]))
                elif cluster != self.assignments[j] and i != j:
                    try:
                        bcluster.setdefault(self.assignments[j], []).append(self.distance[i][j])
                    except TypeError:
                        bcluster.setdefault(self.assignments[j], []).append(self.distance(self.elements[i], self.elements[j]))
            
            if len(asum) < 1:
                si = 0.0
                points[i] = si
                ai = 0.0
            else:
                ai = numpy.mean(asum)
                bi = numpy.min([numpy.mean(v) for _, v in bcluster.items()])
                if ai == 0.0 and bi == 0.0:
                    si = 0.0
                else:
                    si = (bi - ai) / max(ai, bi)
                points[i] = si
                    
        return points
    
