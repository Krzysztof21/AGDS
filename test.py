import graph
import pandas as pd
import numpy as np
import time

def test(database, testfile, printdata = True, func = "mean", k = 5):
    with open(testfile) as csv_file:
        df = pd.read_csv(csv_file)
        data = np.array(df.values.tolist())
        data1 = data[:,0:-1]
        corr = 0
        datalen = len(data1)
        for i in range(datalen):
            if printdata:
                print(data1[i])
                print(i)
            if func == "mean":
                output = database.getClassPredictionMeanSimilarity(data1[i])
            if func == "KNN":
                output = database.getClassPredictionKNN(data1[i], k)
            if func == "KNNF":
                output = database.getClassPredictionKNNFast(data1[i], k, printSimList=False)

            pred = output.index(max(output))+1

            if pred == int(data[i][-1]):
                if printdata:
                    print("CORRECT: prediction: " + str(pred) + ", actual: " + str(int(data[i][-1])) + "\n")
                corr += 1
            else:
                if printdata:
                    print("INCORRECT: prediction: " + str(pred) + ", actual: " + str(int(data[i][-1])) + "\n")
        print("Correct predictions: " + str(corr) + " i.e. " + str(int(100*corr/datalen)) + "%")