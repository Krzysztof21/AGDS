import graph as gr


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
database.addParameters("IrisDataTrain.csv")
database.addColumn("IrisDataTrain.csv", "sle")
database.addColumn("IrisDataTrain.csv", "swi")
database.addColumn("IrisDataTrain.csv", "ple")
database.addColumn("IrisDataTrain.csv", "pwi")
#database.addColumn("IrisDataTrain.csv", "class")

# print(database.maxima)
# database.addValue(8.1, "Param_sle")
# print(database.maxima)
# database.addValue(7.8, "Param_sle")

print(database.graph.Nodes)

