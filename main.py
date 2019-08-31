import graph as gr
import test



#data, datatest  = "CancerDataTrainNorm.csv", "CancerDataTestNorm.csv"

data, datatest  = "IrisDataTrain.csv", "IrisDataTest.csv"

#data, datatest  = "WineDataTrain.csv", "WineDataTest.csv"


database = gr.Database("Base")
database.loadData(data)
print(database.maxima)
print(database.minima)

#print([len(i.edges) for i in database.graph.Nodes if i.type == 'object'])

for k in [5]:
      print(k)
      test.test(database, datatest, func='KNN', printdata=True, k=k)
