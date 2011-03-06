pwum
=============

pwum is a set of python scripts for working on web log files and extracting frequent patterns and clustering sessions. 

Two main functions:

Finding frequent patters - Extract frequently coaccessed pages in sessions. Uses traditonal frequent pattern mining algorithm Apriori. For more information on the implementation, please see [here](http://riivo.net/wp-content/uploads/2011/03/report-pattern-mining-web-logs.pdf)

Finding similar sessions(users)  based on behaviour, find similar users. Clusters users based on navigation. Builds transition chains based pages accesses, measures distance between chains using eucledian distance and clusters by k-means algorithm.
More detailsed description [here](http://riivo.net/wp-content/uploads/2011/03/poster-clustering-web-users.pdf)




Installing
-----------
Tested with Python 2.6
No installation is needed, but there are dependencies:

* numpy
* Pycluster
* matplotlib (optional)


Using pwum
-----------

    python pwum.py [logfile|directory containing only logs]

outputs two html files to `example` folder 




## Some notes
Due to complex nature of the task, the current scripts are not meant for distributed as python package. Currently there are many implemented methods in the code, but there is no convinient configuration availble to select from.

Currently only apache log files in common log format are supported (see data for examples).
logparser.py and logreader.py are responsible for construction session from files. If you have logs with different structure, modify the implementation. logparser currently composes sessions using timeout window.

Some configuration options are availble through config.py editing.

Note this code is meant for prototyping and is not scalable to large amounts of data.



