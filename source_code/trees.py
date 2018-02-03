# encoding=utf-8
'''
Created on Oct 12, 2010
Decision Tree Source Code for Machine Learning in Action Ch. 3
@author: Peter Harrington
'''
from math import log
import operator

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


# create the dataset
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    # change to discrete values
    return dataSet, labels


# 获取数据
def gain_data():
    # fr = open('D:\PyCharm\decision_tree\upload\zhongxiguadata.csv')
    # with open('../upload/zhongxiguadata.csv') as fr:
    with open('D:\PyCharm\decision_tree\upload\zhongxiguadata.csv') as fr:
        lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    # fp = open('D:\PyCharm\decision_tree\upload\labelxigua.txt')
    # with open('/upload/labelxigua.txt') as fp:
    with open('D:\PyCharm\decision_tree\upload\labelxigua.txt') as fp:
        lensesLableses = [inst.strip().split('\t') for inst in fp.readlines()]
        lensesLables = lensesLableses[0]
    # lensesLables = ['seze', 'gendi', 'qiaosheng', 'wenli', 'qibu', 'chugan']
    return lenses, lensesLables


# 将数据集的数组组装成标签
def data_deal():
    data_dict = {}
    lenses, lenses_labels = gain_data()
    for i in range(len(lenses_labels)):
        lab_list = set([example[i] for example in lenses])
        data_dict[lenses_labels[i]] = lab_list
    return data_dict


# calculate the Shannon Entropy
def calcShannonEnt(dataSet):
    # get length
    numEntries = len(dataSet)
    # save the number of every data via dictionary
    labelCounts = {}
    for featVec in dataSet:  # the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)  # log base 2
    return shannonEnt


# according to the given features to split dataset
# axis means the given features , value means return features
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     # chop out axis used for splitting
            # please attention the difference of extend() and append()
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


# choose the best method to split dataset
def chooseBestFeatureToSplit(dataSet):
    # the number of features , and the last column is used for the labels
    numFeatures = len(dataSet[0]) - 1      # the last column is used for the labels
    # calculate the Shannon Entropy
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):        # iterate over all the features
        featList = [example[i] for example in dataSet]# create a list of all the examples of this feature
        uniqueVals = set(featList)       # get a set of unique values
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)     
        infoGain = baseEntropy - newEntropy     # calculate the info gain; ie reduction in entropy
        if infoGain > bestInfoGain:       # compare this to the best gain so far
            bestInfoGain = infoGain         # if better than current best, set to best
            bestFeature = i
    return bestFeature                      # returns an integer


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList): 
        return classList[0]  # stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1:  # stop splitting when there are no more features in dataSet
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    subLabels = labels[:]
    del(subLabels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    num_feat = data_deal()[bestFeatLabel]
    for value in num_feat:
        if value not in uniqueVals:
            myTree[bestFeatLabel][value] = majorityCnt(classList)
            return myTree
        else:
            # subLabels = labels[:]       # copy all of labels, so trees don't mess up existing labels
            myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree                            


def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    # print firstStr
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    # print featIndex
    # print '888'
    key = testVec[featIndex]
    # print key
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        classLabel = valueOfFeat
    return classLabel


def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

