from jinja2 import Environment, PackageLoader, FileSystemLoader
import os
from pystrokes import getStrokeSvgs, getStrokeMap
from flask import Flask, render_template, request
app = Flask(__name__)
 
 
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True
template = env.get_template('index.html')
filename = 'index.html'

@app.route("/")
def form():
  return render_template('form.html')

@app.route("/data/", methods = ['POST', 'GET'])
def data():
  if request.method == 'GET':
    return f"The URL /data is accessed directly. Try going to '/form' to submit form"
  if request.method == 'POST':
    form_data = request.form
    ch = form_data['character']
    svgs = getStrokeSvgs(getStrokeMap(ch))
    return template.render(stroke_svgs = svgs, width = 400, height = 400)
 
app.run(host='localhost', port=5000)
