# -*- coding: utf-8 -*-
# Topic Level Influence #
#########################

from sys import argv
from sys import stdout
import os
from datetime import datetime
import networkx as nx
import influence as inf

#### MAIN ####
script_name, filename, use_weight, normalize = argv
fileout = "output.txt"
script_dir = (os.path.split(os.path.realpath(__file__)))[0] + '/'

# timing start for benchmark
script_start_time = datetime.now()

# use weighting for the metrics?
if use_weight == "0":
     metric_weight = None
else:
     metric_weight = "weight"

# normalize metrics?
if normalize == "0":
    use_norm = False
else:
    use_norm = True

# the top x of any measure, set this to how many values you wish to return
# for example 10 will return the top 10
top_x = 5

# xml fields for use in populating the data
xml_fields = inf.file_XML('PostAuthor', 'AuthorConnection', 'TopicName', 'PostDomain', '/Post')

# check the filetype
file_type = inf.determine_file_type(filename)

# populate lists based on the filetype and xml fields
data_list, topic_list, domain_list = inf.populate_data(filename, xml_fields)

# domain wide influence calculation, so all topics
weight_level = "domain"
inf.adjust_weight(data_list, weight_level)

# output data list to file
# inf.print_to_file(data_list, fileout, filename)

for domain in domain_list:
    #TODO update the runmetric for the domain level
    topic = "All"
    check = 0
    edge_list = []
    for item in data_list:
        # create empty graph
        G = nx.DiGraph()
        # if the domain is in the item
        if (domain == item.domain):
            # add to the graph
            edge_list.append((item.author, item.connection, int(item.weight)))
            check = 1
    #TODO new way to check if a graph isnt empty
    if check == 1:
        # populate the graph
        G.add_weighted_edges_from(edge_list)
        ### generate metrics

        ### degree
        inf.run_metric('Degree', G, domain, topic, metric_weight, use_norm, fileout, top_x)

        ### in degree
        inf.run_metric('In Degree', G, domain, topic, metric_weight, use_norm, fileout, top_x)

        ### out degree
        inf.run_metric('Out Degree', G, domain, topic, metric_weight, use_norm, fileout, top_x)

        ### closeness
        inf.run_metric('Closeness Centrality', G, domain, topic, metric_weight, use_norm, fileout, top_x)

        ### betweenness
        inf.run_metric('Betweenness Centrality', G, domain, topic, metric_weight, use_norm, fileout, top_x)

        ### eigenvector
        inf.run_metric('Eigenvector Centrality', G, domain, topic, metric_weight, use_norm, fileout, top_x)

        ### pagerank
        inf.run_metric('Pagerank', G, domain, topic, metric_weight, use_norm, fileout, top_x)

        inf.create_graphml(G, domain, topic, metric_weight, script_dir)

# script completed
script_end_time = datetime.now()

print "Script completed in: " + str(script_end_time - script_start_time)