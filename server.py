from flask import Flask, render_template, request
from model import learn
import nltk
app = Flask(__name__, static_url_path='/static')

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/req', methods=['GET', 'POST'])
def req():
    return request.method
