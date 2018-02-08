# coding=utf-8
import os
import numpy as np
from sklearn.metrics import accuracy_score, matthews_corrcoef


# 加载本地文本 参数为文件名
def loadDataSet(fileName):
    fr = open(fileName)
    dataMat = []
    labelMat = []
    for eachline in fr.readlines():
        lineArr = []
        curLine = eachline.strip().split('\t')  # remove '\n'   strip():去除首尾空格   split():切片
        # 当前行数据从第4个开始遍历（索引为3）  每行最后一个存标记
        for i in range(0, len(curLine) - 1):
            lineArr.append(curLine[i])  # get all feature from inpurfile
            # lineArr.append(float(curLine[i]))  # get all feature from inpurfile
        dataMat.append(lineArr)
        labelMat.append(curLine[-1])  # last one is class lable
        # labelMat.append(int(curLine[-1]))  # last one is class lable
    fr.close()
    return dataMat, labelMat


# 下面的splitDataSet用来切分数据集，如果是十折交叉，则split_size取10，filename为整个数据集文件，outdir则是切分的数据集的存放路径。
def splitDataSet(fileName, split_size, outdir):
    p = os.path.abspath(outdir)
    import shutil
    shutil.rmtree(p)
    if not os.path.exists(outdir):  # if not outdir , makrdir
        os.makedirs(outdir)
    fr = open(fileName, 'r')  # open fileName to read
    onefile = fr.readlines()  # readlines():返回所有行
    num_line = len(onefile)  # 获取有多少示例(样本)

    arr = np.arange(num_line)  # get a seq and set len=numLine    arange 返回的是一个对象；range 返回的是一个list

    np.random.shuffle(arr)  # generate a random seq from arr    shuftle():随机打乱排序；所有样本都打乱顺序

    list_all = arr.tolist()  # 数组转列表
    each_size = (num_line + 1) / split_size  # size of each split sets   每个有多少数据（样本）
    split_all = []
    each_split = []
    count_num = 0  # count_num 统计每次遍历的当前个数
    count_split = 0  # count_split 统计切分次数
    for i in range(len(list_all)):  # 遍历整个数字序列
        each_split.append(onefile[int(list_all[i])].strip())
        count_num += 1
        if count_num == each_size:
            count_split += 1
            array_ = np.array(each_split)
            np.savetxt(outdir + "/split_" + str(count_split) + '.txt', \
                       array_, fmt="%s", delimiter='\t')  # 输出每一份数据
            split_all.append(each_split)  # 将每一份数据加入到一个list中
            each_split = []
            count_num = 0

    return split_all


# underSample(datafile)方法为抽样函数，强正负样本比例固定为1:1，返回的是一个正负样本比例均等的数据集合
# 下采样  定义：对于一个样值序列间隔几个样值取样一次，这样得到新序列就是原序列的下采样。
def underSample(datafile):  # 只针对一个数据集的下采样
    dataMat, labelMat = loadDataSet(datafile)  # 加载数据

    pos_num = 0  # 正样本数量
    pos_indexs = []  # 正样本位置下标
    neg_indexs = []  # 反样本位置下标
    for i in range(len(labelMat)):  # 统计正负样本的下标
        if labelMat[i] == "是":  # 正样本用  1  表示
            pos_num += 1
            pos_indexs.append(i)  # 正样本的下标
            continue
        neg_indexs.append(i)  # 反样本的下标
    np.random.shuffle(neg_indexs)

    # print neg_indexs

    if len(neg_indexs) >= len(pos_indexs):
        neg_indexs = neg_indexs[0:pos_num]
        fr = open(datafile, 'r')
        onefile = fr.readlines()
        outfile = []
        for i in range(pos_num):
            pos_line = onefile[pos_indexs[i]]
            outfile.append(pos_line)
            # if len(neg_indexs) != 0:
            neg_line = onefile[neg_indexs[i]]
            outfile.append(neg_line)
    else:
        pos_indexs = pos_indexs[0:len(neg_indexs)]
        fr = open(datafile, 'r')
        onefile = fr.readlines()
        outfile = []
        for i in range(len(neg_indexs)):
            pos_line = onefile[pos_indexs[i]]
            outfile.append(pos_line)
            # if len(neg_indexs) != 0:
            neg_line = onefile[neg_indexs[i]]
            outfile.append(neg_line)
    return outfile  # 输出单个数据集采样结果


# 下面的generateDataset(datadir,outdir)方法是从切分的数据集中留出一份作为测试集（无需抽样），对其余的进行抽样然后合并为一个作为训练集
def generateDataset(datadir, outdir):  # 从切分的数据集中，对其中九份抽样汇成一个,剩余一个做为测试集,将最后的结果按照训练集和测试集输出到outdir中
    p = os.path.abspath(outdir)
    import shutil
    shutil.rmtree(p)
    if not os.path.exists(outdir):  # if not outdir , makrdir
        os.makedirs(outdir)
    listfile = os.listdir(datadir)  # os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
    train_all = []
    test_all = []
    cross_now = 0
    for eachfile1 in listfile:
        train_sets = []
        test_sets = []
        cross_now += 1  # 记录当前的交叉次数
        for eachfile2 in listfile:
            if eachfile2 != eachfile1:  # 对其余九份欠抽样构成训练集
                one_sample = underSample(datadir + '/' + eachfile2)
                for i in range(len(one_sample)):
                    train_sets.append(one_sample[i])
        # 将训练集和测试集文件单独保存起来
        with open(outdir + "/test_" + str(cross_now) + ".datasets", 'w') as fw_test:
            with open(datadir + '/' + eachfile1, 'r') as fr_testsets:
                for each_testline in fr_testsets:
                    test_sets.append(each_testline)
            for oneline_test in test_sets:
                fw_test.write(oneline_test)  # 输出测试集
            test_all.append(test_sets)  # 保存测试集
        with open(outdir + "/train_" + str(cross_now) + ".datasets", 'w') as fw_train:
            for oneline_train in train_sets:
                oneline_train = oneline_train
                fw_train.write(oneline_train)  # 输出训练集
            train_all.append(train_sets)  # 保存训练集
    return train_all, test_all


# 因为需要评估交叉验证，所以我写了一个performance方法根据真实类标签纸和预测值来计算SN和SP，当然如果需要其他的评估标准，继续添加即可。
# True Positive （真正, TP）被模型预测为正的正样本；可以称作判断为真的正确率
# True Negative（真负 , TN）被模型预测为负的负样本 ；可以称作判断为假的正确率
# False Positive （假正, FP）被模型预测为正的负样本；可以称作误报率
# False Negative（假负 , FN）被模型预测为负的正样本；可以称作漏报率
# True Positive Rate（真正率 , TPR）或灵敏度（sensitivity） TPR = TP /（TP + FN） 正样本预测结果数 / 正样本实际数
# True Negative Rate（真负率 , TNR）或特指度（specificity） TNR = TN /（TN + FP） 负样本预测结果数 / 负样本实际数
def performance(labelArr, predictArr):  # 类标签为int类型
    # labelArr[i] is actual value,predictArr[i] is predict value
    TP = 0.
    TN = 0.
    FP = 0.
    FN = 0.
    for i in range(len(labelArr)):
        if labelArr[i] == 1 and predictArr[i] == 1:
            TP += 1.
        if labelArr[i] == 1 and predictArr[i] == -1:
            FN += 1.
        if labelArr[i] == -1 and predictArr[i] == 1:
            FP += 1.
        if labelArr[i] == -1 and predictArr[i] == -1:
            TN += 1.
    if FN != 0 or TP != 0:
        SN = TP / (TP + FN)  # 灵敏度 Sensitivity = TP/P  and P = TP + FN
    else:
        SN = 0
    if TN != 0 or FP != 0:
        SP = TN / (FP + TN)  # 特异性 Specificity = TN/N  and N = TN + FP
    else:
        SP = 0
    # MCC = (TP*TN-FP*FN)/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    return SN, SP


# classifier(clf,train_X, train_y, test_X, test_y)方法是交叉验证中每次用的分类器训练过程以及测试过程，
# 里面使用的分类器是scikit-learn自带的。该方法会将一些训练结果写入到文件中并保存到本地，同时在最后会返回ACC,SP,SN。
def classifier(clf, train_X, train_y, test_X, test_y):  # X:训练特征，y:训练标号  clf:学习器
    # train with randomForest
    print " training begin..."
    clf = clf.fit(train_X, train_y)
    print " training end."
    # ==========================================================================
    # test randomForestClassifier with testsets
    print " test begin."
    predict_ =  clf.predict(test_X)  # return type is float64
    proba = clf.predict_proba(test_X)  # return type is float64
    score_ = clf.score(test_X, test_y)
    print " test end."
    # ==========================================================================
    # Modeal Evaluation（评价模型）
    # accuracy_score 分类准确率分数是指所有分类正确的百分比。
    # 形式：sklearn.metrics.accuracy_score(y_true, y_pred, normalize=True, sample_weight=None)
    # normalize：默认值为True，返回正确分类的比例；如果为False，返回正确分类的样本数
    ACC = accuracy_score(test_y, predict_)  # 精度值
    SN, SP = performance(test_y, predict_)
    MCC = matthews_corrcoef(test_y, predict_)  # 马修斯相关系数  得分越高越好
    # AUC = roc_auc_score(test_labelMat, proba)
    # ==========================================================================
    # save output
    eval_output = []
    eval_output.append(ACC)
    eval_output.append(SN)  # eval_output.append(AUC)
    eval_output.append(SP)
    eval_output.append(MCC)
    eval_output.append(score_)
    eval_output = np.array(eval_output)
    # eval_output = np.array(eval_output, dtype=float)
    np.savetxt("proba.data", proba, fmt="%f", delimiter="\t")
    np.savetxt("test_y.data", test_y, fmt="%f", delimiter="\t")
    np.savetxt("predict.data", predict_, fmt="%f", delimiter="\t")
    np.savetxt("eval_output.data", eval_output, fmt="%f", delimiter="\t")
    print "Wrote results to output.data...EOF..."
    return ACC, SN, SP


# 下面的mean_fun用于求列表list中数值的平均值，主要是求ACC_mean,SP_mean,SN_mean，用来评估模型好坏。
def mean_fun(onelist):
    count = 0
    for i in onelist:
        count += i
    return float(count / len(onelist))


# 交叉验证代码
def crossValidation(clf, clfname, curdir, train_all, test_all):
    # 构造出纯数据型样本集
    ACCs = []
    SNs = []
    SPs = []
    cur_path = curdir
    for i in range(len(train_all)):
        if i == 0:
            os.chdir("..")
            os.chdir(cur_path)
        else:
            os.chdir("..")
            os.chdir("..")
            os.chdir("..")
            os.chdir(cur_path)

        train_data = train_all[i]
        train_X = []
        train_y = []
        test_data = test_all[i]
        test_X = []
        test_y = []
        for eachline_train in train_data:
            one_train = eachline_train.split('\t')
            one_train_format = []
            for index in range(0, len(one_train) - 1):
                one_train_format.append(one_train[index])
                # one_train_format.append(float(one_train[index]))
            train_X.append(one_train_format)
            train_y.append(one_train[-1].strip())
            # train_y.append(int(one_train[-1].strip()))
        for eachline_test in test_data:
            one_test = eachline_test.split('\t')
            one_test_format = []
            for index in range(0, len(one_test) - 1):
                one_test_format.append(one_test[index])
                # one_test_format.append(float(one_test[index]))
            test_X.append(one_test_format)
            test_y.append(one_test[-1].strip())
            # test_y.append(int(one_test[-1].strip()))
        # ======================================================================
        # classifier start here
        if not os.path.exists(clfname):  # 使用的分类器
            os.mkdir(clfname)
        out_path = clfname + "/" + clfname + "_00" + str(i + 1)  # 计算结果文件夹
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        os.chdir(out_path)
        ACC, SN, SP = classifier(clf, train_X, train_y, test_X, test_y)
        ACCs.append(ACC)
        SNs.append(SN)
        SPs.append(SP)
        # ======================================================================
    ACC_mean = mean_fun(ACCs)
    SN_mean = mean_fun(SNs)
    SP_mean = mean_fun(SPs)
    # ==========================================================================
    # output experiment result
    os.chdir("../")
    os.system("echo `date` " + str(clf) + " >> log.out")
    os.system("echo ACC_mean=" + str(ACC_mean) + " >> log.out")
    os.system("echo SN_mean=" + str(SN_mean) + " >> log.out")
    os.system("echo SP_mean=" + str(SP_mean) + " >> log.out")
    return ACC_mean, SN_mean, SP_mean


# 外部调用入口
def split_datas(dicot):
    os.chdir("D:/PyCharm/decision_tree/dataDir")  # 你的数据存放目录
    datadir = "split10_1"  # 切分后的文件输出目录
    splitDataSet('zhongxiguadata.txt', dicot, datadir)  # 将数据集datasets切为dicot个保存到datadir目录中
    # ===========================================================================================
    outdir = "sample_data1"  # 抽样的数据集存放目录
    train_all, test_all = generateDataset(datadir, outdir)  # 抽样后返回训练集和测试集
    print "generateDataset end and cross validation start"

# 测试
if __name__ == '__main__':
    os.chdir("dataDir")  # 你的数据存放目录
    datadir = "split10_1"  # 切分后的文件输出目录
    # print os.getcwd()
    splitDataSet('zhongxiguadata.txt', 5, datadir)  # 将数据集datasets切为 （） 个保存到datadir目录中
    # ===========================================================================================
    outdir = "sample_data1"  # 抽样的数据集存放目录
    train_all, test_all = generateDataset(datadir, outdir)  # 抽样后返回训练集和测试集
    print "generateDataset end and cross validation start"
    # ============================================================================================
    # 分类器部分
    # from sklearn.ensemble import RandomForestClassifier
    #
    # clf = RandomForestClassifier(n_estimators=500)  # 使用随机森林分类器来训练（参数：森林里树的个数）
    # clfname = "RF_1"  # ==========================================================================
    # curdir = "experimentdir"  # 工作目录
    # # clf:分类器,clfname:分类器名称,curdir:当前路径,train_all:训练集,test_all:测试集
    # ACC_mean, SN_mean, SP_mean = crossValidation(clf, clfname, curdir, train_all, test_all)
    # print ACC_mean, SN_mean, SP_mean  # 将ACC均值，SP均值，SN均值都输出到控制台
