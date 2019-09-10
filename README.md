# Associative Graph Database System with Classification and Clustering

AGDS is defined and explained in more details in this publicly available lecture by Adrian Horzyk PhD. of AGH UST:
[Knowledge Based Inferences Using Associations AGDS and AVB+ trees](http://home.agh.edu.pl/~horzyk/lectures/ci/CI-KE-KnowledgeBasedInferencesUsingAssociationsAGDSandAVB+trees.pdf)

Three methods for classification were implemented:
1. Mean similarity: given a data record to classify a similarity rate is calculated or every preexisting record in the database, 
accordig to the method outlined in the above lecture. Then a mean similarity rate is calculated for each class and whichever class 
has the highest score, it is assigned to the record in question
2. k Nearest Neighbours: similarity rate is calculated identically as in mean similarity method. Then k data records with the highest 
rate are selected and whichever class is the most frequent in this set, it is assigned to the record in question
3. k Nearest Neighbours Fast: method identical to the above except the similarity rate is calculated only for those data records whose 
parameter values are the closest to the values of the record in question

Datasets used for testing:
1. [Iris dataset](http://archive.ics.uci.edu/ml/datasets/Iris)
2. [Wine dataset](http://archive.ics.uci.edu/ml/datasets/Wine)
3. [Wisconsin Cancer dataset](http://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Original%29)
4. [Glass Identification dataset](http://archive.ics.uci.edu/ml/datasets/Glass+Identification)

Classification accuracy results with k=5 (in percent):

| Dataset\method | Mean similarity | kNN  | kNNF |
| :-------------: | :-------------: | :-----: | :---: |
| Iris      | 58 | 100 | 100 |
| Wine      | 45 | 62 | 70 |
| Cancer | 25 | 80 | 96 |
| Glass  | 15 | 30 | 55 |

Time comparison of the methods:

| Method | Time (s) |
| :---: | :---: |
| Mean | 0.034 |
| kNN | 0.105 |
| kNNF | 0.085 |

Results on Iris dataset, other sets produce similar relations between execution times.

An image representing example of database system with Iris dataset (only x records for clarity of an image):
![alt text](https://github.com/Krzysztof21/AGDS/blob/master/image.JPG   "Iris graph database")
