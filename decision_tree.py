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
from werkzeug.utils import secure_filename

matplotlib.use('Agg')  # 不出现画图的框

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024


fr = open('D:\PyCharm\decision_tree\source_code\listcan.txt')
lenses = [inst.strip().split('\t') for inst in fr .readlines()]
lensesLables = ['seze', 'gendi', 'qiaosheng', 'wenli', 'qibu', 'chugan']


# 生成决策树并画图
def creatpic():
    # fig = plt.figure(1, facecolor='white')
    # lensesLables = ['age', 'prescript', 'astigmatic', 'tearRate']
    lensesTree = trees.createTree(lenses, lensesLables)
    fig = treePlotter.createPlot(lensesTree)
    return fig


@app.route('/dele')
def hello_world():
    # 模板渲染
    return render_template('index.html')


@app.route('/')
def file_upload():
    # 模板渲染
    return render_template('fileupload.html')


# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 处理前台传入的文件
@app.route('/fileup/fileuploaded', methods=["POST"], strict_slashes=False)
def upload_file():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']
    if f and allowed_file(f.filename):
        fname = f.filename
        f.save(os.path.join(file_dir, fname))
        return jsonify({"errno": 0, "errmsg": "上传成功"})
    else:
        return jsonify({"errno": 1001, "errmsg": "上传失败"})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 传入参数,
@app.route('/action/create', methods=['GET'])
# @app.route('/')
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
    attributeList = []
    attributeList.append(requestJsonString['seze'])
    attributeList.append(requestJsonString['gendi'])
    attributeList.append(requestJsonString['qiaosheng'])
    attributeList.append(requestJsonString['wenli'])
    attributeList.append(requestJsonString['qibu'])
    attributeList.append(requestJsonString['chugan'])
    # lensesLablestwo = lensesLables[:]
    lensesTree = trees.createTree(lenses, lensesLables)
    labelsres = trees.classify(lensesTree, lensesLables, attributeList)
    return labelsres


if __name__ == '__main__':
    app.debug = True
    app.run(port=7000, debug=True, threaded=False)