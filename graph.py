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

    def addNode(self, name, type, value, edges = None):
        if edges is None:
            edges = []
        if any(node.name == name for node in self.Nodes):
            print("Node already exists")
        else:
            self.Nodes.append(Node(name, type, value, edges))
            node = self.Nodes[len(self.Nodes)-1]
        return node

    def addEdge(self, name1, name2):
        if (self.getNodeByName(name1) or name1 == "NULL") and (self.getNodeByName(name2) or name2 == "NULL"):
            if name1 == "NULL":
                self.getNodeByName(name2).edges.append(name1)
            if name2 == "NULL":
                self.getNodeByName(name1).edges.append(name2)
            if name1 != "NULL" and name2 != "NULL":
                self.getNodeByName(name1).edges.append(name2)
                self.getNodeByName(name2).edges.append(name1)


    def getNodeByName(self, name):
        for i in range(len(self.Nodes)):
            if self.Nodes[i].name == name:
                node = self.Nodes[i]
                return node
        msg = "Node with <" + str(name) + "> name does not exists"
        #print(msg)
        return None

    def getNodeByValue(self, value, column):
        for i in range(len(self.Nodes)):
            if self.Nodes[i].value == value and self.Nodes[i].edges[0] == column:
                node = self.Nodes[i]
                return node
        msg = "Node with " + str(value) + " value does not exists"
        #print(msg)
        return None

    def getLowerNode(self, name):
        return self.getNodeByName(self.getNodeByName(name).edges[1])

    def getGreaterNode(self, name):
        return self.getNodeByName(self.getNodeByName(name).edges[2])

class Database:

    minima = dict()
    maxima = dict()

    def __init__(self, name):
        self.graph = Graph(name)

    def addParameters(self, filename):
        with open(filename) as csv_file:
            d_reader = csv.DictReader(csv_file)
            headers = d_reader.fieldnames
            print(headers)
            for i in range(len(headers)):
                param = "Param_" + str(headers[i])
                self.graph.addNode(param, "param", headers[i])

    def addValue(self, value, column):
        if self.graph.getNodeByValue(value, column):
            print("Value already exists")
        else:
            name = column + str(value)
            node = self.graph.addNode(name, "value", value)
            self.graph.addEdge(name, column)
            if self.minima.get(column) and node.value < self.minima[column].value:
                self.minima[column].edges[1] = name
                self.graph.addEdge("NULL",  node.name)
                node.edges.append(self.minima[column].name)
                self.minima[column] = node
            if self.maxima.get(column) and node.value > self.maxima[column].value:
                self.maxima[column].edges[2] = name
                node.edges.append(self.maxima[column].name)
                self.graph.addEdge("NULL",  node.name)
                self.maxima[column] = node
            if self.minima.get(column) and self.maxima.get(column) and node.value > self.minima[column].value and node.value < self.maxima[column].value:
                nextNode = self.minima[column]
                while nextNode.value < value:
                    nextNode = self.graph.getGreaterNode(nextNode.name)
                else:
                    node.edges.append(self.graph.getLowerNode(nextNode.name).name)
                    node.edges.append(nextNode.name)
                    self.graph.getLowerNode(nextNode.name).edges[2] = name
                    nextNode.edges[1] = name
            return node

    def addColumn(self, filename, column):
        with open(filename) as csv_file:
            df = pd.read_csv(csv_file)
            saved_column = sorted(list(map(float, set(df[column]))))
            col = "Param_" + str(column)
            for i in range(len(saved_column)):
                if i == 0:
                    self.minima[col] = self.addValue(saved_column[i], col)
                elif i == len(saved_column)-1:
                    self.maxima[col] = self.addValue(saved_column[i], col)
                else:
                    self.addValue(saved_column[i], col)
            for i in range(len(saved_column)):
                if i == 0:
                    self.graph.addEdge("NULL", col+str(saved_column[i]))
                    self.graph.addEdge(col + str(saved_column[i]), col + str(saved_column[i+1]))
                elif i == len(saved_column)-1:
                    self.graph.addEdge(col + str(saved_column[i]), "NULL")
                else:
                    self.graph.addEdge(col + str(saved_column[i]), col + str(saved_column[i + 1]))