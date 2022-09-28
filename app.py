from jinja2 import Environment, PackageLoader, FileSystemLoader
import os
from pystrokes import getStrokeSvgs, getStrokeMap
from flask import Flask, render_template, request
app = Flask(__name__)
 
#template = 'template/index.html'
 
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True
template = env.get_template('index.html')
#filename = os.path.join(root, 'html', 'index.html')
filename = 'index.html'

pngs = [
  "tmp-strokes/stroke_00.png",
  "tmp-strokes/stroke_01.png",
  "tmp-strokes/stroke_02.png",
  "tmp-strokes/stroke_03.png",
  "tmp-strokes/stroke_04.png",
  "tmp-strokes/stroke_05.png",
  "tmp-strokes/stroke_06.png"
]
#ch = '裤'
ch = '姐'

svgs = getStrokeSvgs(getStrokeMap(ch))
print(svgs)

with open(filename, 'w') as fh:
    fh.write(template.render(
#       stroke_pngs = pngs,
        stroke_svgs = svgs,
        width = 400,
        height = 400,
    ))

