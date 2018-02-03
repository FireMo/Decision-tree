import treePlotter
import trees
import os
import chardet

# myDat, labels = trees.createDataSet()
# shannon = trees.calcShannonEnt(myDat)
# print shannon

# print trees.splitDataSet(myDat,0,1)
# print trees.chooseBestFeatureToSplit(myDat)

# fr=open('lenses.txt')
# lenses=[inst.strip().split('\t') for inst in fr.readlines()]
# lensesLables=['age','prescript','astigmatic','tearRate']
# lensesTree= trees.createTree(lenses, lensesLables)
# print lensesTree
# print treePlotter.createPlot(lensesTree)

# fr = open('D:\PyCharm\decision_tree\upload\yingxiguadata.txt')
# with open('../upload/zhongxiguadata.csv') as fr:
#     # print chardet.detect(fr.read())
#     lenses = [inst.strip().split('\t') for inst in fr.readlines()]
# print lenses[0][0]
# fp = open('D:\PyCharm\decision_tree\upload\labelxigua.txt')
# with open('../upload/labelxigua.txt') as fp:
#     lensesLableses = [inst.strip().split('\t') for inst in fp.readlines()]
#     lensesLables = lensesLableses[0]
# print lensesLables[0]
# print chardet.detect(lensesLableses[0][0])

# request = urllib2.Request("http://www.baidu.com")
# response = urllib2.urlopen(request)
# print response.read()
# print os.path.relpath('D:\PyCharm\decision_tree\upload\\xigualabelutf8.txt')
# lenses, lensesLables = trees.gain_data()
# print lenses[0][0]

t = trees.data_deal()
for value in t.values()[0]:
    print value
