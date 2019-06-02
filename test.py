import graph
import pandas as pd
import numpy as np


def test(database, testfile):
    with open(testfile) as csv_file:
        df = pd.read_csv(csv_file)
        data = np.array(df.values.tolist())
        data1 = data[:,0:-1]
        corr = 0
        datalen = len(data1)
        for i in range(datalen):
            print(data1[i])
            output = database.getClassPrediction(data1[i])
            pred = output.index(max(output))+1
            if pred == int(data[i][-1]):
                print("CORRECT: prediction: " + str(pred) + ", actual: " + str(int(data[i][-1])) + "\n")
                corr += 1
            else:
                print("INCORRECT: prediction: " + str(pred) + ", actual: " + str(int(data[i][-1])) + "\n")
        print("Correct predictions: " + str(corr) + " i.e. " + str(int(100*corr/datalen))+ "%")


