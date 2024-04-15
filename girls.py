from flask import Flask, render_template,request, url_for, redirect, flash
# from girlapi import * 
# from extend import * 
from markupsafe import escape



app = Flask(__name__)

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

    girls_list = getgirls()
    return render_template('girls.html', girls_list = girls_list)

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







