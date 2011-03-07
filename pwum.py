# -*- coding: utf_8 -*-
import os, sys
import optparse
from pwum.logs import logreader, logparser
from pwum import  frequent_patterns, clustering, config

import logging.config
logging.config.fileConfig("logging.conf")
log = logging.getLogger()     

def main():
    file_list, support, k = read_opts(sys.argv[1:])
    
    log.info("Parsing input, support: {0}, clusters: {1}".format(support,k ))
    parser = read_and_parse_logs(file_list)

    log.info("Analyzing frequent patterns")
    itemsets_sorted, large_reference_sequence, db_size =  frequent_patterns.analyse_clickstream(parser, support, config.session_filter_fn)
    frequent_patterns.write_output(parser, support, config.PATTERNS_FILE, db_size, itemsets_sorted, large_reference_sequence)
    
    log.info("Clustering")
    clusters, sse = clustering.cluster(parser, k)
    clustering.write_output(k, clusters, sse, config.CLUSTERS_FILE)
    
    log.info("Done!")
    
def read_opts(argv):
    """
    command line options parsing
    """
    
    parser = optparse.OptionParser("usage: %prog [options] logfile")
    parser.add_option("-s", "--support", dest="support",
                      help="relative support, float", default=config.MIN_SUPPORT)
    parser.add_option("-k", "--clusters", dest="clusters",
                      help="number of clusters, integer", default=config.CLUSTERS)
    
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    
    logfile = args[0]
    filelist = []
    
    if os.path.isdir(logfile) :
        filelist = map(lambda x: os.path.join(logfile, x), os.listdir(logfile))
        filelist = filter(lambda x: os.path.isfile(x), filelist)
    elif os.path.isfile(logfile):
        filelist = [logfile]
        
    if len(filelist) == 0:
        parser.error("input is not a file or is empty directory")

    return filelist, float(options.support), int(options.clusters)


def read_and_parse_logs(file_list):
    logfile = logreader.LogFile(logreader.LogLineReader, *file_list)
    parser = logparser.LogParser(logfile)
    parser.parse()
    logfile.close()
    return parser
    
   
if __name__ == "__main__":
    main()
