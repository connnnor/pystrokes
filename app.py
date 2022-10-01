from jinja2 import Environment, PackageLoader, FileSystemLoader
import os
from pystrokes import getStrokeSvgs, getStrokeMap
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def form():
  return render_template('form.html')

@app.route("/stroke")
def stroke():
  ch = request.args.get('character', default = '在', type = str)
  svgs = getStrokeSvgs(getStrokeMap(ch))
  return render_template('index.html', title=f'{ch} Strokes' , stroke_svgs=svgs)

@app.route("/data/", methods = ['POST', 'GET'])
def data():
  if request.method == 'GET':
    return f"The URL /data is accessed directly. Try going to '/form' to submit form"
  if request.method == 'POST':
    form_data = request.form
    # get only 1 character
    ch = form_data['character'][:1]
    # return error if it is not in stroke map
    strokeData = getStrokeMap(ch)
    if strokeData is not None:
      svgs = getStrokeSvgs(strokeData)
      return render_template('index.html', title=f'{ch} Strokes' , stroke_svgs=svgs)
    else:
      return render_template('form.html', form_error=True)
 
app.run(host='localhost', port=5000)
