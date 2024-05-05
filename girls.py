from flask import Flask, render_template,request, url_for, redirect, flash,jsonify
# from girlapi import * 
# from extend import * 
from markupsafe import escape
import os, redis, re
from config import *

# app = Flask(__name__)
app = Flask(__name__)
redis_connections = {
    'red9': redis.Redis(host='localhost', port=6379, db=9),

    'red10': redis.Redis(host='localhost', port=6379, db=10),
    'red11': redis.Redis(host='localhost', port=6379, db=11),
    'red12': redis.Redis(host='localhost', port=6379, db=12),
    'red13': redis.Redis(host='localhost', port=6379, db=13),
    'red14': redis.Redis(host='localhost', port=6379, db=14),
    'red15': redis.Redis(host='localhost', port=6379, db=15)
}


def sort_key(s):
    match = re.search(r'_([0-9]+)', s)
    if match:
        return int(match.group(1))
    return 0  # 如果没有找到匹配项，返回0

def process_infos(redis_connections, condition):
    infos = os.listdir(path)
    print(len(infos))
    # redis_connections['red9'].getkeys()
    newinfos = []
    for info in infos:
        t = redis_connections['red10'].get(info)
        if t is not None:
            t_int = int(t.decode('utf-8'))
            if condition(t_int):
                column = redis_connections['red12'].get(info).decode('utf-8') if redis_connections['red12'].get(info) else None
                name = redis_connections['red13'].get(info).decode('utf-8') if redis_connections['red13'].get(info) else None
                keywords = redis_connections['red14'].get(info).decode('utf-8') if redis_connections['red14'].get(info) else None
                description = redis_connections['red15'].get(info).decode('utf-8') if redis_connections['red15'].get(info) else None
                newinfos.append({'info': info, 'column': column, 'name': name, 'keywords': keywords, 'description': description})
    print(len(newinfos))
    return newinfos


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
    return redirect('/')

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

def main_condition(t_int):
    return  t_int >= 60

def index_condition(t_int):
    return t_int == 50


@app.route('/main', methods=['GET', 'POST'])
def main():
    newinfos = process_infos(redis_connections, main_condition)
    return render_template('xiutaku.html', infos=newinfos)

@app.route('/', methods=['GET', 'POST'])
def index():
    newinfos = process_infos(redis_connections, index_condition)
    return render_template('xiutaku.html', infos=newinfos)



@app.route('/xiutakugirl/<string:name>')
def xiutakugirl(name):
    redis_connections['red10'].set(name, 60)

    imagesdir = os.path.join(path, name)
    images = os.listdir(imagesdir)
    # 排序列表
    images = sorted(images, key=sort_key)
    # print(images)
    images = [os.path.join(name, _) for _ in images]
    # print(images)
    column = redis_connections['red12'].get(name).decode('utf-8') if redis_connections['red12'].get(name) else None
    girl = redis_connections['red13'].get(name).decode('utf-8') if redis_connections['red13'].get(name) else None
    keywords = redis_connections['red14'].get(name).decode('utf-8') if redis_connections['red14'].get(name) else None
    description = redis_connections['red15'].get(name).decode('utf-8') if redis_connections['red15'].get(name) else None
    print(column)
    print(girl)
    print(keywords)
    print(description)

    
    return render_template('xiutakualbumn.html', images = images, girl = girl,
            column  = column,   keywords = keywords, description = description      )


@app.route('/delete_albumn', methods = ['POST'])
def delete_albumn():
    name = request.json.get("itemID")
    
    print(name)
    red = redis.Redis(host='localhost', port=6379, db=10)
    red.set(name, 0)
    response = {"status": "success", "message": "Item deleted successfully"}
    return jsonify(response)
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







