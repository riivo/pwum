# -*- coding: utf_8 -*-

import logging.config
logging.config.fileConfig("logging.conf")
log = logging.getLogger()     


import getopt, os, sys
from pwum.logs import logreader, logparser
from pwum import  frequent_patterns, clustering, config


def main():
    log.info( "Starting up..")
    file_list, sigma = read_opts(sys.argv[1:])
    log.info("Parsing input")
    parser = read_and_parse_logs(file_list)

    log.info("Analyzing clickstream")
    frequent_patterns.analyse_clickstream(parser, sigma, config.session_filter_fn, config.PATTERNS_FILE)
    
    log.info("Clustering")
    clustering.cluster(parser, 10, config.CLUSTERS_FILE)
    
    log.info("Done!")
    
def read_opts(argv):
    """
    command line options parsing
    """
    logfile = None #single file or directory"
    support = config.MIN_SUPPORT  
    try:
        opts, args = getopt.getopt(argv, 's:', ["support"])
        if len(args) == 0:
            raise getopt.GetoptError("No log file, directory") 
        if len(args) == 1:
            logfile = args[0]
        
        for o, a in opts:
            if o in ("-s", "--support"):
                support = float(a)
                if support > 1.0 or support < 0 : 
                    raise getopt.GetoptError("Support must be between 0<suppoty<=1.0") 
            else:
                raise getopt.GetoptError("incompatible arguments")


    except getopt.GetoptError, err:
        print "Error: " + str(err)
        usage()
        sys.exit(2)    
 
    if logfile is not None:
        if os.path.isdir(logfile) :
            filelist = map(lambda x: os.path.join(logfile, x), os.listdir(logfile))
            filelist = filter(lambda x: os.path.isfile(x), filelist)
        else:
            filelist = [logfile]
    
    return filelist, support


def usage():
    print "usage: python pwum.py logfile [options]"
    print "OPTIONS:"
    print "\t s, --support: float - support for frequent pattern mining,\
             relative, default {0}".format(config.MIN_SUPPORT)



def read_and_parse_logs(file_list):
    log_file_reader = lambda x: logreader.LogLineReader(x)
    logfile = logreader.LogFile(log_file_reader, *file_list)
    parser = logparser.LogParser(logfile)
    parser.parse()
    logfile.close()
    return parser
    
   
if __name__ == "__main__":
    main()
