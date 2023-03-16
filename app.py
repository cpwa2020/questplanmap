from functions import *

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map', methods=['GET','POST'])
def map():
    if request.method == 'POST':
        lat = float(request.form.get('lat'))
        lon = float(request.form.get('lon'))
        url = request.form.get('url')
        lst = routesnear(lat,lon,url)
        return render_template('map.html',lst=lst)
    else:
        return 'Incorrect HTTP method', 400

@app.route('/plan', methods=['GET','POST'])
def plan():
    if request.method == 'POST':
        id = request.form.get('id')
        lst = tripsroute(id)
        return render_template('plan.html',lst=lst)
    else:
        return 'Incorrect HTTP method', 400

if __name__=='__main__':
   app.run()