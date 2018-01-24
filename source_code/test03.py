import treePlotter
import trees

# myDat, labels = trees.createDataSet()
# shannon = trees.calcShannonEnt(myDat)
# print shannon

# print trees.splitDataSet(myDat,0,1)
# print trees.chooseBestFeatureToSplit(myDat)

fr=open('lenses.txt')
lenses=[inst.strip().split('\t') for inst in fr.readlines()]
lensesLables=['age','prescript','astigmatic','tearRate']
lensesTree= trees.createTree(lenses, lensesLables)
print lensesTree
print treePlotter.createPlot(lensesTree)





# request = urllib2.Request("http://www.baidu.com")
# response = urllib2.urlopen(request)
# print response.read()


