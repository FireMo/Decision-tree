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

fr = open('D:\PyCharm\decision_tree\upload\\xiguadata3utf8.txt')
# print chardet.detect(fr.read())
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
print lenses
fp = open('D:\PyCharm\decision_tree\upload\\xigualabelutf8.txt')
lensesLableses = [inst.strip().split('\t') for inst in fp.readlines()]
# print chardet.detect(lensesLableses[0][0])
# print lensesLableses
# request = urllib2.Request("http://www.baidu.com")
# response = urllib2.urlopen(request)
# print response.read()
print os.path.relpath('D:\PyCharm\decision_tree\upload\\xigualabelutf8.txt')

