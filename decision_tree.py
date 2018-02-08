# encoding=utf-8
import base64
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib
from source_code import treePlotter, trees
from flask import Flask, url_for, request, make_response, json, redirect, abort, session,\
    render_template_string, render_template, send_from_directory, jsonify
from source_code import trees
from source_code import testdemo, rawdata
from werkzeug.utils import secure_filename
import json
import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


matplotlib.use('Agg')  # 不出现画图的框
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))  # D:\PyCharm\decision_tree
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

# g_fattr = " "
# g_fvalue = " "


# 模板渲染
@app.route('/')
def hello_world():
    attr_dicts = rawdata.data_deal()
    return render_template('index.html', attribute=attr_dicts)


# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 处理前台传入的文件
# @app.route('/fileup/fileuploaded', methods=["POST"], strict_slashes=False)
@app.route('/fileup/fileuploaded', methods=["POST"])
def upload_file():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    attr_dict = rawdata.data_deal()
    fattr = request.files['fileattr']
    # g_fattr = fattr
    fvalue = request.files['filevalue']
    # g_fvalue = fvalue
    if fattr and fvalue and allowed_file(fattr.filename) and allowed_file(fvalue.filename):
        fattrname = fattr.filename
        fvaluename = fvalue.filename
        fattr.save(os.path.join(file_dir, fattrname))
        fvalue.save(os.path.join(file_dir, fvaluename))
        # return jsonify({"success": 0, "successmsg": "上传成功"})
        results = "上传成功！"
        return render_template('upfileresult.html', attribute=attr_dict, results=results)
    else:
        # return jsonify({"error": 1001, "errmsg": "上传失败"})
        results = "请检查文件！"
        return render_template('upfileresult.html', attribute=attr_dict, results=results)


# g_fattr = request.files['fileattr']
# print g_fattr
# print '*********'
# print g_fvalue


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 生成决策树并画图
def creatpic():
    lenses_more = rawdata.get_more_train_data()
    lenses_labels = rawdata.get_attr_value()
    lenses_tree = trees.createTree(lenses_more, lenses_labels)
    fig = treePlotter.createPlot(lenses_tree)
    return fig


# 获取交叉验证结果
@app.route('/cv/result', methods=["POST"])
def cross_vali():
    foldnum = request.form.get("foldnum", type=int, default=5)
    # print type(foldnum)
    from source_code import crossv
    crossv.split_datas(foldnum)
    test_labs, accuracies, correct_ratio = testdemo.gain_results(foldnum)
    # print '真实标签值为：%s; 决策树检测的标签为：%s' % (test_labs[0][0], accuracies[0][0])
    # return test_labs, accuracies, correct_ratio
    return render_template('cvres.html', test_labs=test_labs, accuracies=accuracies, correct_ratio=correct_ratio)


# 模板渲染
@app.route('/sss')
def file_upload():
    # attr_labels = {}
    # lenses, lenses_labels = trees.gain_data()
    attr_dict = rawdata.data_deal()
    # attr_labels['label'] = lenses_labels
    # attr_labels['valuess'] = attr_dict['']
    return render_template('fileupload.html', labels=attr_dict)


# 传入参数
@app.route('/action/create', methods=['GET'])
def index():
    fig = creatpic()
    # Encode image to png in base64
    sio = BytesIO()
    fig.savefig(sio, format='png')
    data = base64.b64encode(sio.getvalue()).decode()
    return data


@app.route('/action/dealdata', methods=['POST'])
def dealdata():
    requestJsonString = request.form.to_dict()
    butlist = []
    attributeList = []
    attr_dict = rawdata.data_deal()
    lenses_more = rawdata.get_more_train_data()
    lenses_labels = rawdata.get_attr_value()
    for i in range(len(lenses_labels)):
        for labelc in attr_dict.keys():
            if labelc == lenses_labels[i]:
                attributeList.append(requestJsonString[labelc])
                break
    for i in range(len(attributeList)):
        butlist.append(attributeList[i].encode('utf-8'))
    lensesTree = trees.createTree(lenses_more, lenses_labels)
    labelsres = trees.classify(lensesTree, lenses_labels, butlist)
    return render_template('index.html', attribute=attr_dict, labelsres=labelsres)


if __name__ == '__main__':
    app.debug = True
    app.run(port=7000, debug=True, threaded=False)
