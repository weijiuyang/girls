from flask import Flask, render_template,request, url_for, redirect, flash
from girlapi import * 
from extend import * 
from markupsafe import escape



app = Flask(__name__)

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'


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
    return render_template('girl.html', albumns = albumns)

@app.route('/albumn', methods=['GET', 'POST'])
def albumn():
    albumn_id = request.args.get('albumn_id') 
    images = getalbumn(albumn_id)[:2]
    return render_template('albumnview.html', images = images)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3333', debug=True)






