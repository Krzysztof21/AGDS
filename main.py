import graph as gr
import test


data, datatest  = "IrisDataTrain.csv", "IrisDataTest.csv"

#data, datatest  = "WineDataTrain.csv", "WineDataTest.csv"

#data, datatest  = "CancerDataTrain.csv", "CancerDataTest.csv"

#data, datatest  = "CancerDataTrainNorm.csv", "CancerDataTestNorm.csv"


database = gr.Database("Base")

database.loadData(data)

for k in [5]:
      print(k)
      test.test(database, datatest, func='KNNF', printdata=True, k=k)

