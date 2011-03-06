pwum
=============

This a set of python scripts for working on web log files and extracting frequent patterns and clustering sessions. 

Two main functions:

Finding frequent patters - Extract frequently coaccessed pages in session. Uses traditonal frequent pattern mining algorithm Apriori. For more information on the implementation, please refer to:
http://riivo.net/wp-content/uploads/2011/03/report-pattern-mining-web-logs.pdf

Finding similar sessions(users)  based on behaviour, find similar users. Clusters users based on navigation. Different methods are available, but by default following method is used. http://riivo.net/wp-content/uploads/2011/03/poster-clustering-web-users.pdf




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

outputs two html files to examplefolder where pwum was run




## Some notes
Due to complex nature of the task, the current scripts are not meant for distributed as python package. Currently there are many implementation methods in the code, but there is no convinient configuration availble to select from.

Currently only supports apache log files in common log format (see data for examples).
logparser.py and logreader.py are responsible for construction session from files. If you have logs with different structure, modify the implementation. logparser currently composes sessions using timeout window.

Some configuration options are availble through config.py editing.

Note this code is meant for prototyping and is not scalable to large amounts of data.



