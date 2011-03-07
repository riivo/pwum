import Pycluster
import numpy

import pwum.algorithms.clustering.modeling as session_modeling
from pwum import config
from pwum.algorithms.clustering import kmeans
from pwum.util import output
from pwum.algorithms import string_similarity


def cluster(parser, k):
    """
    general method for clustering data
    """
    
    #get index number for every page
    code_book = parser.get_data_encoding(page_min_occurance=5)
    
    #use only sequence of pages visited
    simple_session = [session for session in parser.get_simple_sessions() if config.session_filter_fn(session)]
    
    #use vector representation (v1,v2,v2) where v1 means page v1 was visited    
    #models = session_modeling.convert_sessions_to_vector(simple_session, code_book, binary=True)
    
    #construct markov chains, estimate transition probabilities
    models = session_modeling.convert_sessions_to_markov(simple_session, code_book, bayes=False)
    idx, sse, _ = Pycluster.kcluster(models, k, method='a', dist='e')
 
    #idx, sse, _ = cluster_kmedoids(models, k, string_similarity.jaccard_distance)
    

    clusters = {}
    for name, clusterid in zip(simple_session, idx):
        clusters.setdefault(clusterid, []).append(name)
    
    return clusters, sse
    
def write_output(k,clusters, sse, filename):    
    out = output.Ouput()
    
    out.h1("Clustering results")
    out.p("Clusters, k= {0}".format(k))
    out.p("SSE(sum of squared errors)= {0}".format(sse))
    out.p("somma separates pages in sessions")
    
    for centroid_id, cluster_session in clusters.items():
        out.h1("Cluster {0}: item count {1} ".format(centroid_id,len(cluster_session) ))

        out.table()
        cluster_session2 = sorted(cluster_session)
        for annotation in cluster_session2:
            out.tr([", ".join(annotation) ]) 
        out.end_table()
        out.hr()

    out.to_file(filename)


def compute_distances(sessions, distance_fn):
    """
    compute distance matrix between sessions
    """
    nlen = len(sessions)
    distances = numpy.zeros((nlen, nlen), numpy.float)
    
    for i in range(nlen):
        for j in range(0, i):
            distances[i][j] = distances[j][i] = distance_fn(sessions[i], sessions[j])
    return distances


def cluster_kmedoids(sessions, clusters, distance_fn=string_similarity.jaccard_distance):
    """
    kmedoids clustering, requires distance matrix, therefore slow
    """
    distances = compute_distances(sessions, distance_fn)
    clusterids, error, nfound = Pycluster.kmedoids(distances, nclusters=clusters)
    return clusterids, error, nfound



