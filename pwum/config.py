"""
some global constants
"""

#min support for pattern mining, relative
MIN_SUPPORT = 0.06
CLUSTERS = 20


HOME_PAGE = "/"
SESSION_TIMEOUT = 1800 #session timeout in seconds

##following parameters don't apply to parser, parser still gives out all data

#----------------------------------------#
#pattern minign specigin
#filter sessions with fewer than 2 clicks
session_filter_fn = lambda x: len(x) > 2 
#name of the output file
PATTERNS_FILE = "examples/frequent_patters.html"


#----------------------------------------#
#clustering

#number of times page has to be present to be used in feature vector representation
PAGE_MIN_OCCURANCE = 3
CLUSTERS_FILE="examples/clusters.html"