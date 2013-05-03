# Readme for influence.py
# Influence prototype for use on network data that uses the networkx package http://networkx.github.com/
#
# Usage
# Ensure that there is a "plots" directory at the same level as the influence.py script.
#
# You will need to pass the filename and then a 0 or 1 at the command line.  
# 0 for unweighted, 1 for weighted.  
# Example: python influence.py <FILENAME> 0 #for unweighted
# Example: python influence.py <FILENAME> 1 #for weighted
#
# Included test files are testing data, and from the stanford large data set collection 
# http://snap.stanford.edu/data/.
#
# (>>>NOTE<<< - Latest updates have broken support for the Stanford large dataset files, its next on the TODO list to fix this.  Email me if you would like some test data). Use the attached text files (test, Epinions, Gnutella) to run through the sample calculations
#
# Limitations: 
# Ensure that there is a "plots" directory at the same level as the influence.py script.
# Currently pulls data from files only
#
# New features:
# >Graphml output of connection data
# >Support for Domain and topic level decomposition of data
# >Support for weighted AND unweighted calculations

# Known issues:
# >Support for Stanford large data sets is currently disabled

# ToDos included in influence.py
