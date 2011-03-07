import operator

from pwum.algorithms import apriori, sequences
from pwum.util import output, time_decorator

def analyse_clickstream(parser, support, session_filter_fn):
    """
    finds frequent patterns from parser and stores in filename
    """
    transactions = [session for session in parser.get_simple_sessions() if session_filter_fn(session)]
    db_size = len(transactions)
    
    min_support = int(db_size  * support)+1
    itemsets, supports = apriori.apriori(transactions, min_support)
    
    itemsets_sorted = sorted(supports.iteritems(), key=operator.itemgetter(1), reverse=True)
    large_reference_sequence, _ = sequences.large_reference_sequences(transactions, min_support)

    
    return itemsets_sorted, large_reference_sequence, db_size
    
def write_output(parser, support, filename, db_size, itemsets_sorted, large_reference_sequence):
    ###write out to file
    out = open_output(parser, db_size, support)
    out.h1("Frequent itemset: ")
    out.table()
    out.tr(["support", "itemsets"])
    for itemset, support in itemsets_sorted:
        relative_support = 1.0 * support / db_size
        out.tr([str(round(relative_support, 2)), ", ".join(itemset)])
    
    out.end_table()
    out.hr()
    out.h1("Large reference sequences: ")
    out.table()
    for r in large_reference_sequence:
        out.tr([" -> ".join(r)])
    
    out.end_table()
    out.hr()
    out.to_file(filename)
    
def open_output(parser, db_size, support):
    out = output.Ouput()
    out.h1("Some statistics")
    out.p("Sessions: {0}".format(len(parser.sessions.keys())))
    out.p("Matching lines: {0}".format(parser.count))
    out.p("Number of different urls: {0}".format(len(parser.pages)))
    out.p("DB size after reduction: {0}".format(db_size))
    out.p("Support {0}".format(support))    
    return out
