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

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        nodes = [i.name for i in self.edges if not isinstance(i, str)]
        return "\nName: " + str(self.name) + ", type: " + str(self.type) + ", value: " + str(self.value) + ", connected nodes: " + str(nodes) + ", similarity index: " + str(self.rate) + '\n'


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
            node = Node(name, type, value, edges)
            self.Nodes.append(node)
        return node

    def delNode(self, name):
        pass

    def addEdge(self, node1, node2):

        if node1 and node2:
            if node1 == "NULL":
                node2.edges.append(node1)
            if node2 == "NULL":
                node1.edges.append(node2)
            if node1 != "NULL" and node2 != "NULL":
                node2.edges.append(node1)
                node1.edges.append(node2)

    def delEdge(self):
        pass

    def getNodeByName(self, name):
        for node in self.Nodes:
            if node.name == name:
                return node
        return None

    def getNodeByValue(self, value, column):
        '''

        :param value: [string] Value of the column parameter to be searched
        :param column: [Node object] Column to be searched
        :return: Node object if found
                 None if not found
        '''
        for node in column.edges:
            if node.value == value:
                return node
        return None

    def getParamNode(self, node, param):
        '''

        :param node: [Node object] Data object
        :param param: [Node object] Parameter of data object to be found
        :return: Node object representing parameter value
        '''
        for value in node.edges:
            if param.name in value.name:
                return value

    def getLowerNode(self, node):

        return node.edges[1]

    def getGreaterNode(self, node):

        return node.edges[2]

class Database:

    minima = dict()
    maxima = dict()
    parameterNodes = []

    def __init__(self, name):
        self.graph = Graph(name)
        self.objectCount = 0

    #
    #LOADING SECTION
    #

    def loadData(self, filename):
        self.graph.Nodes = []
        self.addParameters(filename)
        self.addObjects(filename)

    def addParameters(self, file):
        with open(file) as csv_file:
            d_reader = csv.DictReader(csv_file)
            self.headers = d_reader.fieldnames
            print(self.headers)
            for i in range(len(self.headers)):
                name = "Param_" + str(self.headers[i])
                print(name)
                column = self.graph.addNode(name, "param", self.headers[i])
                self.parameterNodes.append(column)
                self.addColumn(file, column)

    def addObjects(self, file):
        '''Adding objects (specific row of data)

        :param file: opened file from calling namespace
        :return: None
        '''
        with open(file) as csv_file:
            obj = pd.read_csv(csv_file).values
            for i in range(len(obj)):
                self.addSingleObject(obj[i, :])

    def addColumn(self, file, column):
        '''Adding all values of a parameter, deleting duplicates, saving minimum and maximum

        :param file: opened file from calling namespace
        :param column: object of type Node, representing name of a parameter of data
        :return: None
        '''
        df = pd.read_csv(file)
        saved_column = sorted(list(map(float, set(df[column.name[6:]]))))

        tempNode = self.addValue(saved_column[0], column)
        for i in range(len(saved_column)):
            if i == 0:
                node = self.addValue(saved_column[i + 1], column)
                self.minima[column.name] = tempNode
                self.graph.addEdge("NULL", tempNode)
                self.graph.addEdge(tempNode, node)
            elif i == len(saved_column)-1:
                self.maxima[column.name] = tempNode
                self.graph.addEdge(tempNode, "NULL")
                break
            else:
                node = self.addValue(saved_column[i + 1], column)
                self.graph.addEdge(tempNode, node)
            tempNode = node

    def addValue(self, value, column):
        '''Adding value node, updating minima or maxima if neccessary

        :param value: Value of the parameter to be added (possibly str or numerical)
        :param column: Appropriate parameter node
        :return: Node object, if created correctly

        '''
        alreadyNode = self.graph.getNodeByValue(value, column)
        if alreadyNode:
            return alreadyNode
        else:
            name = column.name + str(value)
            node = self.graph.addNode(name, "value", value)
            self.graph.addEdge(node, column)
            if self.minima.get(column.name) and node.value < self.minima[column.name].value:
                self.minima[column.name].edges[1] = node
                self.graph.addEdge("NULL",  node)
                node.edges.append(self.minima[column.name])
                self.minima[column.name] = node
            if self.maxima.get(column.name) and node.value > self.maxima[column.name].value:
                self.maxima[column.name].edges[2] = name
                node.edges.append(self.maxima[column.name])
                self.graph.addEdge("NULL",  node)
                self.maxima[column.name] = node
            if self.minima.get(column.name) and self.maxima.get(column.name) and node.value > self.minima[column.name].value and node.value < self.maxima[column.name].value:
                nextNode = self.minima[column.name]
                while nextNode.value < value:
                    nextNode = self.graph.getGreaterNode(nextNode)
                else:
                    prevNode = self.graph.getLowerNode(nextNode)
                    node.edges.append(prevNode)
                    node.edges.append(nextNode)
                    prevNode.edges[2] = node
                    nextNode.edges[1] = node
            return node

    def delValue(self, node):
        column = node.edges[0]
        if not node:
            return "Value already deleted"
        if len(node.edges) > 3:
            return "Value still used"
        if node.edges[1] == "NULL":
            tempNode = self.graph.getGreaterNode(node)
            tempNode.edges[1] = 'NULL'
            self.minima[column.name] = tempNode
        elif node.edges[2] == "NULL":
            tempNode = self.graph.getLowerNode(node)
            tempNode.edges[2] = 'NULL'
            self.maxima[column.name] = tempNode
        else:
            self.graph.getGreaterNode(node).edges[1] = node.edges[1]
            self.graph.getLowerNode(node).edges[2] = node.edges[2]
        if node in self.graph.Nodes:
            self.graph.Nodes.remove(node)

    def addSingleObject(self, fields):
        '''Adds single object with given parameters values

        :param fields: Paramteres of added object
        :return: Node object
        '''
        name = "Obj" + str(self.objectCount)
        node = self.graph.addNode(name,"object", None)
        for i in range(len(fields)):
            param = self.addValue(fields[i], self.parameterNodes[i])
            if param:
                self.graph.addEdge(node, param)
        self.objectCount += 1
        return node

    def delSingleObject(self, node):
        if not node:
            return "Object already deleted"
        for param in node.edges:
            param.edges.remove(node)
            if len(param.edges) < 4:
                self.delValue(param)
        self.graph.Nodes.remove(node)


    #
    #ANALYTICS SECTION
    #

    def getAverage(self, column):
        param = self.graph.getNodeByName("Param_"+str(column))
        sum = 0
        count = 0
        for i in range(len(param.edges)):
            node = param.edges[i]
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
                node = self.graph.getGreaterNode(node)

    def setParamSimilarity(self, node, column):
        '''Given a node and a parameter, method calculates similarity for each value of parameter'''
        param = self.graph.getParamNode(node, column)
        temp = param.rate
        param.rate = 1
        low = self.graph.getLowerNode(param)
        high = self.graph.getGreaterNode(param)
        rang = self.maxima[column.name].value-self.minima[column.name].value

        while low != "NULL":
            weight = 1 - abs(param.value-low.value)/rang
            low.rate = temp * weight
            temp = low.rate
            param = low
            low = self.graph.getLowerNode(param)

        param = self.graph.getParamNode(node, column)
        temp = param.rate

        while high != "NULL":
            weight = 1-abs(param.value-high.value)/rang
            high.rate = temp * weight
            temp = high.rate
            param = high
            high = self.graph.getGreaterNode(param)

    def setKParamSimilarity(self, node, column, k):
        '''
        Given a node and a parameter, method calculates
        similarity for ~k nearest values of parameter
        '''
        param = self.graph.getParamNode(node, column)
        param.rate = 1
        temp = param.rate
        low = self.graph.getLowerNode(param)
        high = self.graph.getGreaterNode(param)
        rang = self.maxima[column.name].value - self.minima[column.name].value
        kRange = m.ceil(k/2)
        i = 0

        while low != "NULL" and i < kRange:
            weight = 1 - abs(param.value - low.value) / rang
            low.rate = temp * weight
            temp = low.rate
            param = low
            low = self.graph.getLowerNode(param)
            i += 1

        param = self.graph.getParamNode(node, column)
        temp = param.rate

        i = 0
        while high != "NULL" and i < kRange:
            weight = 1 - abs(param.value - high.value) / rang
            high.rate = temp * weight
            temp = high.rate
            param = high
            high = self.graph.getGreaterNode(param)
            i += 1

    def setObjectRate(self, node):
        factor = 1/(len(self.maxima)-1)
        if node.rate == 0:
            for param in (n for n in node.edges if n.type == 'value'):
                node.rate += factor * param.rate
        return node.rate

    def getSimilarity(self, node):
        for param in self.parameterNodes:
            if param.name != "Param_class":
                self.setParamSimilarity(node, param)
        corr = len(self.headers) / (len(self.headers) - 1)
        similarNodes = dict()
        for obj in self.graph.Nodes:
            if obj.type == "object":
                similarNodes[obj.name] = self.setObjectRate(obj)
        names = sorted(similarNodes.items(), key=lambda x: x[1], reverse=True)
        objList = []
        for i in names:
            objList.append(self.graph.getNodeByName(i[0]))
        return objList

    def getKSimilarity(self, node, k):
        for param in self.parameterNodes:
            if param.name != "Param_class":
                self.setKParamSimilarity(node, param, k)

        similarNodes = dict()
        j = 0
        for value in self.graph.Nodes:
            #if j >= 2*k:
            #    break
            if value.rate != 0 and value.type == "value":
                for i in range(len(value.edges)):
                    if i > 2:
                        temp = value.edges[i]
                        similarNodes[temp.name] = self.setObjectRate(temp)
                        j += 1
        names = sorted(similarNodes.items(), key=lambda x: x[1], reverse=True)
        objList = []
        for i in names:
            objList.append(self.graph.getNodeByName(i[0]))
        return objList

    def getClassPredictionMeanSimilarity(self, fields):
        '''
        Class predicted by calculating mean similarity rate
        between given data and each class.
        '''
        node = self.addSingleObject(fields)
        for i in range(len(fields)):
            self.setParamSimilarity(node, self.parameterNodes[i])
        corr = len(self.headers)/(len(self.headers)-1)
        classes = self.parameterNodes[-1].edges
        prediction = [0] * len(classes)
        counts = [0] * len(classes)
        for obj in self.graph.Nodes:
            if obj.type == "object" and node.name != obj.name:
                for i in range(len(prediction)):
                    if obj.edges[len(self.headers)-1] == classes[i]:
                        prediction[i] += self.setObjectRate(obj)*corr
                        counts[i] += 1
        for i in range(len(prediction)):
            prediction[i] = prediction[i]/counts[i]
        self.delSingleObject(node)
        for nd in self.graph.Nodes:
            nd.rate = 0
        return prediction

    def getClassPredictionKNN(self, fields, k):
        '''
        Class predicted with k nearest neighbours algorithm
        '''
        node = self.addSingleObject(fields)
        classes = self.parameterNodes[-1].edges
        prediction = [0] * len(classes)
        simList = self.getSimilarity(node)
        for i in range(k):
            for j in range(len(prediction)):
                if simList[i].edges[-1] == classes[j]:
                    prediction[j] += 1
        for i in range(len(prediction)):
            prediction[i] = prediction[i]/k
        self.delSingleObject(node)
        for nd in self.graph.Nodes:
            nd.rate = 0
        return prediction

    def getClassPredictionKNNFast(self, fields, k, printSimList = False):
        '''
        Class predicted with k nearest neighbours algorithm
        with calculations performed for only the nearest points
        '''
        node = self.addSingleObject(fields)
        #print(self.graph.Nodes)
        classes = self.parameterNodes[-1].edges
        prediction = [0] * len(classes)
        simList = self.getKSimilarity(node,k)
        if printSimList:
            print(simList[:(k+1)])
            print("SimList length: " + str(len(simList)))
        for i in range(k):
            for j in range(len(prediction)):
                if simList[i].edges[-1] == classes[j]:
                    prediction[j] += 1
        for i in range(len(prediction)):
            prediction[i] = prediction[i]/k
        self.delSingleObject(node)
        for nd in self.graph.Nodes:
            nd.rate = 0
        return prediction



    def getDiffPrediction(self, fields):
        node = self.addSingleObject(fields.append(1))
        simVal = self.getSimilarity(node)
