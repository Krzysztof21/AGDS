import csv
import pandas as pd

class Node:

    def __init__(self, name, type, value, edges):
        self.name = name
        self.type = type
        self.value = value
        self.edges = edges

    def __repr__(self):
        return "\nName: " + str(self.name) + ", type: " + str(self.type) + ", value: " + str(self.value) + ", connected nodes: " + str(self.edges)



class Graph:

    Nodes = []

    def __init__(self, name="Default"):
        self.name = name

    def addNode(self, name, type, value, edges = []):
        if any(node.name == name for node in self.Nodes):
            print("Node already exists")
        else:
            self.Nodes.append(Node(name, type, value, edges))

    def addEdge(self, name1, name2):
        if self.getNodeByName(name1) and self.getNodeByName(name2):
            self.getNodeByName(name1).edges.append(name2)
            self.getNodeByName(name2).edges.append(name1)

    def getNodeByName(self, name):
        for i in range(len(self.Nodes)):
            if self.Nodes[i].name == name:
                node = self.Nodes[i]
                return node
        msg = "Node with <" + str(name) + "> name does not exists"
        print(msg)
        return None

    def getNodeByValue(self, value, column):
        for i in range(len(self.Nodes)):
            if self.Nodes[i].value == value and self.Nodes[i].edges[0] == column:
                node = self.Nodes[i]
                return node
        msg = "Node with " + str(value) + " value does not exists"
        print(msg)
        return None

class Database:

    def __init__(self, name):
        self.graph = Graph(name)

    def addParameters(self, filename):
        with open(filename) as csv_file:
            d_reader = csv.DictReader(csv_file)
            headers = d_reader.fieldnames
            print(headers)
            for i in range(len(headers)):
                param = "Param" + str(i)
                self.graph.addNode(param, "param", headers[i])

    def addValue(self, value, column):
        if self.graph.getNodeByValue(value, column):
            print("Value already exists")
        else:
            name = column + str(value)
            self.graph.addNode(name, "value", value, [column])


    def addColumn(self, filename, column):
        with open(filename) as csv_file:
            df = pd.read_csv(csv_file)
            saved_column = sorted(list(map(float, set(df[column]))))
            for i in range(len(saved_column)):
                self.addValue(saved_column[i], column)
