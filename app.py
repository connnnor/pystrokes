import argparse
from flask import Flask, render_template, request
from pystrokes import getStrokeSvgs, getStrokeMap
import pinyin
from waitress import serve
app = Flask(__name__)

MAX_NUM_CHARS = 16

parser = argparse.ArgumentParser(description='run pystrokes webserver')
parser.add_argument('--host', type=str, default='localhost', help='flask host')
parser.add_argument('--port', type=int, default=8080, help='flask port')

@app.route("/")
def form():
  return render_template('form.html')

@app.route("/stroke")
def stroke():
  chars = request.args.get('character', default = '在', type = str)
  return render_strokes_template(chars)

@app.route("/data/", methods = ['POST'])
def data():
  form_data = request.form
  return render_strokes_template(form_data['characters'])

def render_strokes_template(inputChars):
  inputChars = inputChars[:MAX_NUM_CHARS]
  if len(inputChars) < 1:
    return render_template('form.html', form_error=True)
  strokeData = []
  for ch in inputChars:
    strokeDict = getStrokeMap(ch)
    if strokeDict is None:
      return render_template('form.html', form_error=True)
    svgs = getStrokeSvgs(strokeDict)
    strokeData.append({'character' : ch, 'strokes' : svgs, 'pinyin' : pinyin.get(ch)})
  return render_template('index.html', data=strokeData, title=f'{inputChars} Strokes')

args = parser.parse_args()
serve(app, host=args.host, port=args.port)
