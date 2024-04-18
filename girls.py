from flask import Flask, render_template,request, url_for, redirect, flash
# from girlapi import * 
# from extend import * 
from markupsafe import escape
import os, redis, re


# app = Flask(__name__)
app = Flask(__name__, static_folder='/home/weijiuyang/spider')



def sort_key(s):

    match = re.search(r'_([0-9]+)', s)
    if match:
        return int(match.group(1))
    return 0  # 如果没有找到匹配项，返回0



@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'


@app.route('/xiutaku', methods=['GET', 'POST'])
def xiutaku():
    infos = ['cake','girl','beaty']
    return render_template('xiutaku.html', infos=infos)

@app.route('/test', methods=['GET', 'POST'])
def test():
    albumn_id = 917
    images = getalbumn(albumn_id)
    return render_template('test3.html', images = images)

@app.route('/new', methods=['GET', 'POST'])
def new():
    images = randomalbumn()
    # albumn_id = 1042
    # images = getalbumn(albumn_id)
    # print(images)
    return render_template('albumnnew.html', images = images)

@app.route('/favorite', methods=['GET', 'POST'])
def favorite():
    val = request.get_json()
    id = val["id"]
    level = val["level"]
    status = favorite_sql(id,level)
    return r'success'

@app.route('/delimg', methods=['GET', 'POST'])
def delimg():
    val = request.get_json()
    id = val["id"]
    status = delimg_sql(id)
    return r'success'

@app.route('/', methods=['GET', 'POST'])
def index():
    path = '../spider/image'
    infos = os.listdir(path)
    print(infos)
    red = redis.Redis(host='localhost', port=6379, db=10)
    newinfos = []
    for info in infos:
        t = red.get(info)
        if t is not None:  # 检查是否有值
            t_int = int(t.decode('utf-8'))  # 先解码成字符串，然后转换成整数
            print(t_int)
            print(t_int > 30)
            if t_int > 30:
                newinfos.append(info)
    # infos = ['cake','girl','beaty']
    return render_template('xiutaku.html', infos = newinfos)
    girls_list = getgirls()
    return render_template('girls.html', girls_list = girls_list)


@app.route('/xiutakugirl/<string:name>')
def xiutakugirl(name):
    path = '/home/weijiuyang/spider/image'
    # name = request.args.get('name') 
    imagesdir = os.path.join(path, name)
    images = os.listdir(imagesdir)


    # 排序列表
    images = sorted(images, key=sort_key)
    print(images)
    images = [os.path.join(name, _) for _ in images]
    print(images)
    return render_template('xiutakualbumn.html', images = images, albumn = name)


@app.route('/delete_albumn', methods = ['POST'])
def delete_albumn():
    name = request.json.get("itemID")
    
    print(name)
    red = redis.Redis(host='localhost', port=6379, db=10)
    red.set(name, 0)
    return 'fff'
    images = [os.path.join(name, _) for _ in images]
    print(images)
    return render_template('xiutakualbumn.html', images = images, albumn = name)

@app.route('/girl', methods=['GET', 'POST'])
def girl():
    girl = request.args.get('girl') 
    page = request.args.get('page') 
    if page == None:
        page = 1
    albumns = getgirl(girl,page)
    return render_template('girl.html', girl = girl, page = page, albumns = albumns)

@app.route('/albumn', methods=['GET', 'POST'])
def albumn():
    albumn_id = request.args.get('albumn_id') 
    images = getalbumn(albumn_id)
    return render_template('albumnview.html', images = images)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port='3333', debug=True)
    app.run(host='::', port='3333', debug=True)







