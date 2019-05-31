import graph as gr
from datetime import datetime

# node1 = gr.Node("Node1", "param", "sle", [])
#
# print(node1)
#
# graph1 = gr.Graph("Ir")
#
# graph1.addNode("Node1", "param", "sle")
# graph1.addNode("Node2", "param", "ple")
#
# print(graph1.Nodes)
#
# graph1.addEdge("Node1", "Node2")
#
# print(graph1.Nodes)

database = gr.Database("Iris")
# database.addParameters("IrisDataTrain.csv")
# database.addColumn("IrisDataTrain.csv", "sle")
# database.addColumn("IrisDataTrain.csv", "swi")
# database.addColumn("IrisDataTrain.csv", "ple")
# database.addColumn("IrisDataTrain.csv", "pwi")
# #setosa = 1, versicolor = 2, virginica = 3
# database.addColumn("IrisDataTrain.csv", "class")

# print(database.maxima)
# database.addValue(8.1, "Param_sle")
# print(database.maxima)
# database.addValue(7.8, "Param_sle")

#database.addSingleObject([5.1,3.5,1.4,0.2,1.0])
#database.addObjects("IrisDataTrain.csv")
database.loadData("IrisDataTrain.csv")
#print(database.graph.Nodes)
print(database.getAverage('sle'))

# node = database.graph.getNodeByName("Obj150")
# t1 = datetime.now()
# a = database.getSimilarity(node)
# t2 = datetime.now()
# delta = t2 - t1
# print(delta.total_seconds())

#print(a[1:10])

node = database.addSingleObject([7.8,3.5,0.9,2.6,1.0])
print(database.graph.Nodes)
database.delSingleObject(node.name)
print(database.graph.Nodes)