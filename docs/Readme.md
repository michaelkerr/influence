# Readme for influence.py
# Influence prototype for use on network data
# Use the attachd text files (test, Epinions, Gnutella) to run through the sample caluclations
# to change the input file simple put the path in the "filename" on line 12
#
# Limitations: 
# Gnutella file works quite quickly (all measures in less than 2 minutes), larger data files become exponentially larger as the adjacency matrix does (# of authors and edges)
# The last lines of the code:
     ### connection plot
     ### nx.draw_spring(G)
     ### plt.show()
# plot the connection data and are EXTREMELY intensive when using large data set.  Suggest only use with the test.txt or with IO xml files
