import functions

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map', methods=['GET','POST'])
def map():
    return render_template('map.html')
    