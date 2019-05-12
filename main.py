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
print(database.graph.Nodes)
database.addColumn("IrisDataTrain.csv", "sle")
print(database.graph.Nodes)

print(database.graph.getNodeByName("sle7.6"))
print(database.graph.getNodeByName("sle7.5"))
print(database.graph.getNodeByValue(7.6, "sle"))
print(database.graph.getNodeByValue(7.8, "sle"))