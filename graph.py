import csv
import pandas as pd
import math as m

class Node:

    def __init__(self, name, type, value, edges):
        self.name = name
        self.type = type
        self.value = value
        self.edges = edges
        self.rate = 0

    def __repr__(self):
        return "\nName: " + str(self.name) + ", type: " + str(self.type) + ", value: " + str(self.value) + ", connected nodes: " + str(self.edges) + ", similarity index: " + str(self.rate)


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

    def delNode(self, name):
        pass

    def addEdge(self, name1, name2):
        if (self.getNodeByName(name1) or name1 == "NULL") and (self.getNodeByName(name2) or name2 == "NULL"):
            if name1 == "NULL":
                self.getNodeByName(name2).edges.append(name1)
            if name2 == "NULL":
                self.getNodeByName(name1).edges.append(name2)
            if name1 != "NULL" and name2 != "NULL":
                self.getNodeByName(name1).edges.append(name2)
                self.getNodeByName(name2).edges.append(name1)

    def delEdge(self):
        pass

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

    def getParamNode(self, node, param):
        for i in range(len(node.edges)):
            if param in node.edges[i]:
                return self.getNodeByName(node.edges[i])

    def getLowerNode(self, name):
        return self.getNodeByName(self.getNodeByName(name).edges[1])

    def getGreaterNode(self, name):
        return self.getNodeByName(self.getNodeByName(name).edges[2])

class Database:

    minima = dict()
    maxima = dict()

    def __init__(self, name):
        self.graph = Graph(name)
        self.objectCount = 0

    def loadData(self, filename):
        self.addParameters(filename)
        self.addObjects(filename)

    def addParameters(self, filename):
        with open(filename) as csv_file:
            d_reader = csv.DictReader(csv_file)
            self.headers = d_reader.fieldnames
            print(self.headers)
            for i in range(len(self.headers)):
                param = "Param_" + str(self.headers[i])
                self.graph.addNode(param, "param", self.headers[i])
                self.addColumn(filename, self.headers[i])

    def addValue(self, value, column):
        if self.graph.getNodeByValue(value, column):
            #print("Value already exists")
            return None
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

    def delValue(self, name):
        param = self.graph.getNodeByName(name)
        col = name[6:9]
        if not param:
            return "Value already deleted"
        if len(param.edges) > 3:
            return "Value still used"
        if param.edges[1] == "NULL":
            self.minima[col] = self.graph.getGreaterNode(name).edges[1] = 'NULL'
        elif param.edges[2] == "NULL":
            self.maxima[col] = self.graph.getLowerNode(name).edges[2] = 'NULL'
        else:
            self.graph.getGreaterNode(param.name).edges[1] = param.edges[1]
            self.graph.getLowerNode(param.name).edges[2] = param.edges[2]
        self.graph.Nodes.remove(param)

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

    def addSingleObject(self, fields):
        self.objectCount += 1
        name = "Obj" + str(self.objectCount)
        node = self.graph.addNode(name,"object", None)
        for i in range(len(fields)):
            param = self.addValue(fields[i],"Param_"+str(self.headers[i]))
            if param:
                self.graph.addEdge(name, param.name)
            else:
                self.graph.addEdge(name, "Param_"+str(self.headers[i])+str(fields[i]))
        return node

    def delSingleObject(self, name):
        node = self.graph.getNodeByName(name)
        if not node:
            return "Object already deleted"
        for paramName in node.edges:
            param = self.graph.getNodeByName(paramName)
            param.edges.remove(name)
            if len(param.edges) < 4:
                self.delValue(paramName)
        self.graph.Nodes.remove(node)


    def addObjects(self, filename):
        with open(filename) as csv_file:
            obj = pd.read_csv(csv_file).values
            for i in range(len(obj)):
                self.addSingleObject(obj[i,:])

    def getAverage(self, column):
        param = self.graph.getNodeByName("Param_"+str(column))
        sum = 0
        count = 0
        for i in range(len(param.edges)):
            node = self.graph.getNodeByName(param.edges[i])
            sum += node.value*(len(node.edges)-3)
            count += len(node.edges)-3
        return sum/count

    def getMedian(self, column):
        node = self.minima["Param_" + str(column)]
        c = 0
        if self.objectCount % 2 == 0:
            middle = m.floor(self.objectCount/2)
            while c != middle:
                c += (len(node.edges)-3)
                node = self.graph.getGreaterNode(node.name)

    def setSimilarityValues(self, node, column):
        '''Given a node and a parameter method calculates similarity for each value of parameter'''
        param = self.graph.getParamNode(node, column)
        temp = param.rate
        param.rate = 1
        low = self.graph.getLowerNode(param.name)
        high = self.graph.getGreaterNode(param.name)
        rang = self.maxima["Param_"+column].value-self.minima["Param_"+column].value

        while low:
            weight = 1 - abs(param.value-low.value)/rang
            low.rate = temp * weight
            temp = low.rate
            param = low
            low = self.graph.getLowerNode(param.name)

        param = self.graph.getParamNode(node, column)
        temp = param.rate

        while high:
            weight = 1-abs(param.value-high.value)/rang
            high.rate = temp * weight
            temp = high.rate
            param = high
            high = self.graph.getGreaterNode(param.name)

    def setObjectRate(self, node):
        factor = 1/len(self.maxima)
        for param in node.edges:
            node.rate += factor * self.graph.getParamNode(node, param).rate
        return node.rate

    def getSimilarity(self, node):
        for param in self.headers:
            self.setSimilarityValues(node, param)
        similarNodes = dict()
        for obj in self.graph.Nodes:
            if obj.type == "object":
                similarNodes[obj.name] = self.setObjectRate(obj)
        names = sorted(similarNodes.items(), key=lambda x: x[1], reverse=True)
        objList = []
        for i in names:
            objList.append(self.graph.getNodeByName(i[0]))
        for nd in self.graph.Nodes:
            nd.rate = 0
        return objList

    def getClassPrediction(self, fields):
        node = self.addSingleObject(fields)
        for i in range(len(fields)):
            self.setSimilarityValues(node, self.headers[i])
        similarNodes = dict()
        corr = len(self.headers)/(len(self.headers)-1)
        prediction = [0] * len(self.graph.getNodeByName("Param_class").edges)
        counts = [0] * len(self.graph.getNodeByName("Param_class").edges)
        for obj in self.graph.Nodes:
            if obj.type == "object":
                similarNodes[obj.name] = self.setObjectRate(obj)*corr
                if node.name != obj.name:
                    for i in range(len(prediction)):
                        if obj.edges[len(self.headers)-1] == self.graph.getNodeByName("Param_class").edges[i]:
                            prediction[i] += similarNodes[obj.name]
                            counts[i] += 1
        for i in range(len(prediction)):
            prediction[i] = prediction[i]/counts[i]
        self.delSingleObject(node.name)
        for nd in self.graph.Nodes:
            nd.rate = 0
        return prediction
