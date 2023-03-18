from functions import *

from flask import Flask, render_template, request, send_file

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
        iid = request.form.get('id')
        aid = request.form.get('aid')
        lst = tripsroute(aid,iid)
        return render_template('plan.html',lst=lst)
    else:
        return 'Incorrect HTTP method', 400

@app.route('/folmap')
def folmap():
    return send_file('static/mpm.html')

@app.route('/fnctns', methods=['POST'])
def fnctns():
    lctnh = request.form.get('lctnh')
    lctns = request.form.get('lctns')
    lctnw = request.form.get('lctnw')
    lctno = request.form.get('lctno')
    svlctn(lctnh,lctns,lctnw,lctno)
    return 'Processed', 204

if __name__=='__main__':
   app.run()