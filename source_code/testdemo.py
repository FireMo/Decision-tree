# -*- coding:utf8 -*-
import crossv
import trees
import rawdata
import treePlotter
import os
# basedir = os.path.abspath(os.path.dirname(__file__))


# 获取结果
def gain_results(foldnum):
    # 获取属性列表
    lenses_labels = rawdata.get_attr_value()
    dirs = os.listdir('D:/PyCharm/decision_tree/dataDir/sample_data1')
    decision_trees = []
    accuracies = []
    tests = dirs[:foldnum]  # 测试集
    trains = dirs[-foldnum:]  # 训练集
    for i in range(len(trains)):
        lenses = rawdata.get_train_data(trains[i])
        decision_tree = trees.createTree(lenses, lenses_labels)
        # print treePlotter.createPlot(decision_tree)  # 循环打印决策树
        decision_trees.append(decision_tree)
    # print len(decision_trees)  # 5
    # print treePlotter.createPlot(decision_trees)
    for m in range(len(tests)):
        accu = []
        decs_tree = decision_trees[m]
        test_data = rawdata.get_test_data(tests[m])
        # print decs_tree  # 决策树
        # print test_data  # 被测数据
        for y in range(len(test_data)):
            result = trees.classify(decs_tree, lenses_labels, test_data[y][:-1])
            accu.append(result)
        accuracies.append(accu)
    test_labs = []
    correct_ratio = []
    for p in range(len(tests)):
        test_lab = []
        test_data = rawdata.get_test_data(tests[p])
        for t in range(len(test_data)):
            test_lab.append(test_data[t][-1])
        test_labs.append(test_lab)
    # print test_labs[4][0]
    # print len(test_labs)
    for w in range(len(tests)):
        count = 0.0
        for q in range(len(test_labs[w])):
            # print '真实标签值为：%s; 决策树检测的标签为：%s' % (test_labs[w][q], accuracies[w][q])
            if test_labs[w][q] == accuracies[w][q]:
                count += 1
        # print '正确率为：%f' % (count/(len(test_labs[w])))
        ratio = count/(len(test_labs[w]))
        correct_ratio.append(ratio)
    return test_labs, accuracies, correct_ratio









