from pystrokes import getStrokeSvgs, getStrokeMap
from flask import Flask, render_template, request
app = Flask(__name__)

MAX_NUM_CHARS = 4

@app.route("/")
def form():
  return render_template('form.html')

@app.route("/stroke")
def stroke():
  chars = request.args.get('character', default = '在', type = str)
  return render_strokes_template(chars)

@app.route("/data/", methods = ['POST', 'GET'])
def data():
  if request.method == 'GET':
    return f"The URL /data is accessed directly. Try going to '/form' to submit form"
  if request.method == 'POST':
    form_data = request.form
    return render_strokes_template(form_data['characters'])

def render_strokes_template(inputChars):
    inputChars = inputChars[:MAX_NUM_CHARS]
    if len(inputChars) < 1:
        return render_template('form.html', form_error=True)
    data = []
    for ch in inputChars:
      strokeDict = getStrokeMap(ch)
      if strokeDict is None:
        return render_template('form.html', form_error=True)
      svgs = getStrokeSvgs(strokeDict)
      data.append({'character' : ch, 'strokes' : svgs})
    return render_template('index.html', data=data, title=f'{inputChars} Strokes')
 
app.run(host='localhost', port=5000)
