#### Influence Calculations ###
# Created Date: 2013/01/03
# Last Updated: 2013/03/18

#TODO break out into libraries
#TODO redesign connections
#TODO fix import to work with Stanford large data sets, imports those as ints and not strings....
#TODO turn into a service
#TODO django front end for interaction and visualization
#TODO add automated testing
#TODO interactive metric calculation
#TODO combine output file and graphml into a single .zip file and name accordingly
#TODO database (Mongo, SOLR) interface support
#TODO output results to a DB
#TODO Sort data to come out in domain, topic order - list then comma delimited?

#### RESOURCES -----------------------------------------------------------------------------------###
from sys import argv
from sys import stdout
import os
import libxml2
import networkx as nx
from datetime import datetime
import itertools

#### Classes -------------------------------------------------------------------------------------###     
class file_XML(object):
     def __init__(self, child1, child2, child3, child4, child5):
	  self.child1 = child1
	  self.child2 = child2
	  self.child3 = child3
	  self.child4 = child4
	  self.child5 = child5
	  
class author_entry(object):
     def __init__(self, domain, topic, author, connection, weight):
	  self.domain = domain
	  self.topic = topic
	  self.author = author
	  self.connection = connection
	  self.weight = weight	  
	  
#### FUNCTIONS -----------------------------------------------------------------------------------###     
def determine_file_type(filename):
     #determines the type of file
     extension = filename.split('.')[1]
     if extension == 'txt':
	  file_type = 'SLDS txt'
     elif extension == 'xml':
	  file_type = 'IO xml'
     return file_type
     
def create_graphs(topics):
     # creates the appropriate number of graphs base don number of topics
     net_graphs = []
     return net_graphs
     
def populate_data(filename, xml_fields):
     # populates a list from a Standford Large Data Set file (modified)
     file_type = determine_file_type(filename)
     # if the file is a text file_type
     if file_type == 'SLDS txt':
	  entry_list, topic_list, domain_list = populate_from_text(filename)	  
     # if the file is an XML file_type
     elif file_type == 'IO xml':
	  # populate the edge list(s)
	  entry_list, topic_list, domain_list = populate_from_xml(filename)
     return entry_list, topic_list, domain_list


def populate_from_text(filename):
     # populates list from a text file
     entry_list = []
     topic_list, domain_list = ["None"], ["None"]
     with  open(filename,'r') as data_file:
	  for line in data_file:
	       if '#' not in line:
		    i = int(line.split(',')[0]) + 1
		    j = int(line.split(',')[1]) + 1
		    entry_list.append(author_entry("None", "None", i, j, 1))
	  if data_file.closed != True:
	       data_file.close()
     entry_list = adjust_weight(entry_list)
     return entry_list, topic_list, domain_list
     
def populate_from_xml(filename):
     with open(filename,'r') as data_file:
	  doc = libxml2.parseDoc(data_file.read())
	  root = doc.children
	  child = root.children
	  # temporary list to store (topic, connection)
	  entry_list, author_list, topic_name, topic_list, domain_list = [], [], [], [], []
	  for child in root:
	       if (child.type == 'element' and child.name == 'PostAuthor'):
		    author_name = (child.content).decode('utf_8')
	       if (child.type == 'element' and child.name == 'TopicName'):
		    topic_name = (child.content).decode('utf_8')
		    if (child.content).decode('utf_8') not in topic_list:
			 topic_list.append((child.content).decode('utf_8'))
	       if (child.type == 'element' and child.name == 'AuthorConnection'):
		    author_list.append((topic_name, (child.content).decode('utf_8')))
	       if (child.type == 'element' and child.name == 'PostDomain'):
		    # TODO if there are topics with author connections 
		    for entry in author_list:
			 if entry[1] != '':
			      #split the authors
			      temp_list = entry[1].split(',')
			      for item in temp_list:
				   #remove the "-#" at the end of each name
				   item = item.split('-')
				   entry_list.append(author_entry((child.content).decode('utf_8'), entry[0], author_name, item[0], 1))
			      if (child.content) not in domain_list:
			         domain_list.append((child.content).decode('utf_8'))
		    author_list = []
	  if data_file.closed != True:
	       data_file.close()
	  entry_list = adjust_weight(entry_list)
     return entry_list, topic_list, domain_list

def author_entry_key_function(author_entry):
     return (author_entry.domain, author_entry.topic, author_entry.author, author_entry.connection)

def adjust_weight(data_list):
     inf_list=[]
     for key, subiter in itertools.groupby(data_list, author_entry_key_function):
          inf_list.append(author_entry(key[0], key[1], key[2], key[3], sum(ae.weight for ae in subiter)))
     return inf_list
     
'''
def adjust_weight(data_list):
     inf_list=[]
     for entry in data_list:
	  count = 0
	  for item in data_list:
	       if entry.domain == item.domain and entry.topic == item.topic and entry.author == item.author and entry.connection == item.connection and entry.weight == item.weight:
		    count += 1
	  inf_list.append(author_entry(entry.domain, entry.topic, entry.author, entry.connection, count))
     return list(set(inf_list))
'''

def run_metric(metric_name, G, domain, topic, metric_weight, fileout, top_x):
     print '\n>> ' + metric_name + ' for ' + domain + " - " + topic
     
     start_time = datetime.now()
     
     if metric_name == 'Degree':
	  graph_metric = G.degree(nbunch=None, weight=metric_weight)
	  # the degree is the sum of the edge weights adjacent to the node
     elif metric_name == 'In Degree':
	  graph_metric = G.in_degree(nbunch=None, weight=metric_weight)
	  # the degree is the sum of the edge weights adjacent to the node
     elif metric_name == 'Out Degree':
	  graph_metric = G.out_degree(nbunch=None, weight=metric_weight)
	  # the degree is the sum of the edge weights adjacent to the node
     elif metric_name == 'Closeness Centrality':
	  graph_metric = nx.closeness_centrality(G, distance=None, normalized=False) # use distance as weight? to increase importance as weight increase distance = 1/weight
     elif metric_name == 'Betweenness Centrality':
	  graph_metric = nx.betweenness_centrality(G, normalized=False, weight=metric_weight) # 
     elif metric_name == 'Eigenvector Centrality':
	  try: 
	       graph_metric = nx.eigenvector_centrality(G, max_iter=1000)
	  except nx.exception.NetworkXError:
	       # use numpy eigenvector if fail to converge
	       print "power method for calculating eigenvector did not converge, using numpy"
	       graph_metric = nx.eigenvector_centrality_numpy(G)
     elif metric_name == 'Pagerank':
	  #TODO add weights pagerank
	  try:
	       graph_metric = nx.pagerank(G, weight=metric_weight)
	  except:
	       # use numpy if fails to converge
	       print "power method for calculating pagerank did not converge, using numpy"
	       graph_metric = nx.pagerank_numpy(G, weight=metric_weight)
     end_time = datetime.now()
     print "Calculation completed in: " + str(end_time - start_time)

     # append the entire list to the output file
     append_to_file(graph_metric, fileout, domain, topic, metric_name)
     
     # convert to a list of tuples
     graph_metric = graph_metric.items()
     # sort
     graph_metric.sort(key=lambda tup: -tup[1]) 
     # get and print the top X
     # print metric_results(graph_metric)
     top_list =  take(top_x, graph_metric)
     for item in top_list:
	  print ((item[0]) + "," + str(item[1]))
     return
     
def metric_results(graph_metric):
     metric_topx_list = graph_metric #take(top_x, graph_metric)
     for item in metric_topx_list:
	  #TODO dont print "None" after each list
	  #TODO fix order issue - if RTL number comes up first
	  print (item[0]) + ' ' + str(item[1])
	  
def take(n, iterable):
     # Return first n items of the iterable as a list
     return list(itertools.islice(iterable, n))
     
def print_to_file(data_list, fileout, filename):
     with open(fileout,'w') as output_file: 
	  output_file.write('>>>DATA LIST FOR: ' + filename + '\n')
	  for entry in data_list:
	       output_file.write((entry.domain).encode('utf_8') + ", " + (entry.topic).encode('utf_8') + ", " + (entry.author).encode('utf_8') + ", " + (entry.connection).encode('utf_8') + ", " + str(entry.weight) + "\n")
	  output_file.write('\n>>>GRAPH METRICS\n')
     if output_file.closed != True:
	  output_file.close()
     return
     
def append_to_file(graph_metric, fileout,  domain, topic, metric_name):
     with open(fileout,'a') as output_file: 
	  #output_file.write('\n' + domain + ' - ' + topic + '\n' + metric_name + '\n' + '-------------------------' + '\n')
	  graph_list = graph_metric.items()
	  for item in graph_list:
	       #output_file.write((item[0]).encode('utf_8') + "," + str(item[1]) + '\n')
	       output_file.write(domain.encode('utf_8') + "," + topic.encode('utf_8') + "," + metric_name + "," + (item[0]).encode('utf_8') + "," + str(item[1]) + '\n')
     if output_file.closed != True:
	  output_file.close()	  
     return

def build_graphml_name(domain, topic, metric_weight, script_dir):
     if metric_weight == "weight":
	  graphml_filename = str(script_dir) + 'plots/' + str(domain) + '_' + str(topic).replace("/", "") + '_' + 'Weighted' + '.graphml'
     else:
	  graphml_filename = str(script_dir) + 'plots/' + str(domain) + '_' + str(topic).replace("/", "") + '_' + 'Unweighted' + '.graphml'
     if " " in graphml_filename:
	  graphml_filename = graphml_filename.replace(" ", "_")
     return graphml_filename
#### MAIN ----------------------------------------------------------------------------------------###
script_name, filename, use_weight = argv
fileout = "output.txt"
script_dir = (os.path.split(os.path.realpath(__file__)))[0] + '/'

# timing start for benchmark
script_start_time = datetime.now()

# use weighting for the metrics?
if use_weight == "0":
     metric_weight = None
else:
     metric_weight = "weight"
     
# the top x of any measure, set this to how many values you wish to return 
# for example 10 will return the top 10
top_x = 5

# xml fields for use in populating the data
xml_fields = file_XML('PostAuthor', 'AuthorConnection', 'TopicName', 'PostDomain', '/Post')

# check the filetype
file_type = determine_file_type(filename)

# populate lists based on the filetype and xml fields
data_list, topic_list, domain_list = populate_data(filename, xml_fields)

# output data list to file
print_to_file(data_list, fileout, filename)

for domain in domain_list:
     for topic in topic_list:
	  check = 0
	  edge_list = []
	  for item in data_list:
	       # create empty graph
	       G = nx.DiGraph()
	       # if the domain and topic are in the item
	       if (item.domain == domain and item.topic == topic):
		    # add to the graph
		    edge_list.append((item.author, item.connection, int(item.weight)))
		    check = 1
	  ##TODO find a working way to check if a graph isnt empty  		    
	  if check == 1:
	       G.add_weighted_edges_from(edge_list)
	       ### generate metrics
	       
	       ### degree
	       run_metric('Degree', G, domain, topic, metric_weight, fileout, top_x)
	       
	       ### in degree
	       run_metric('In Degree', G, domain, topic, metric_weight, fileout, top_x)
	       
	       ### out degree
	       run_metric('Out Degree', G, domain, topic, metric_weight, fileout, top_x)
	       
	       ### closeness
	       run_metric('Closeness Centrality', G, domain, topic, metric_weight, fileout, top_x)
	       
	       ### betweenness
	       run_metric('Betweenness Centrality', G, domain, topic, metric_weight, fileout, top_x)
	       
	       ### eigenvector
	       run_metric('Eigenvector Centrality', G, domain, topic, metric_weight, fileout, top_x)

	       ### pagerank
	       run_metric('Pagerank', G, domain, topic, metric_weight, fileout, top_x)
	       
	       graphml_filename = build_graphml_name(domain, topic, metric_weight, script_dir)
	       
	       nx.write_graphml(G,graphml_filename,prettyprint=True)
	       

# script completed
script_end_time = datetime.now()

print "Script completed in: " + str(script_end_time - script_start_time)