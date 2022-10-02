import json
from cairosvg import svg2png
from PIL import Image
import math
import io
import pinyin
import mizige
import argparse

parser = argparse.ArgumentParser(description='generate stroke sequence images for characters')
parser.add_argument('characters', type=str, help='one or more chinese characters')

svgCodeTemplate = """
<svg viewBox="0 0 1024 1024">
  <g transform="scale(1, -1) translate(0, -900)">
    {STROKES}
  </g>
</svg>
"""

svgPathTemplate = """
<path fill="{COLOR}" d="{DATA}"></path>
"""

ELEM_HEIGHT = 1024
ELEM_WIDTH  = 1024

GRID_COLS = 6

GraphicsPath = 'graphics.txt'
ResultsPath = 'strokes/{pn}_{ch}_strokes.png'
mizigePath =  './mizige.png'

# keys = character, strokes, medians
strokeMap = {}

def getStrokeMap(character):
  with open(GraphicsPath, "r") as f:
    for line in f:
      patternString = f'"character":"{character}"'
      if patternString in line:
        return json.loads(line)
    return None


def getStrokeSvgs(strokeMap):
  strokes = strokeMap["strokes"]
  strokesSvg = [] 
  for i in range(0, len(strokes)):
    svgPaths = []
    for j in range(0, i+1):
      color = "red" if i == j else "black"
      svgPaths.append(svgPathTemplate.format(COLOR=color,DATA=strokes[j]))
    strokesSvg.append('\n'.join(svgPaths))
  return strokesSvg

def addBackgroundImage(fgImg, bgImg, color="WHITE"):
  newImg = Image.new(("RGBA"), fgImg.size, color=color)
  newImg.alpha_composite(bgImg, (0, 0))
  newImg.alpha_composite(fgImg, (0, 0))
  newImg.convert('RGBA')
  return newImg

def imageGrid(imgs, rows, cols, color="WHITE"): 
    assert len(imgs) <= rows*cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h), color=color)
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

def writeStrokePng(svgs, cols, filename):
  rows = math.ceil(len(svgs) / cols)
  backgroundImg = Image.open(mizigePath)
  # convert svgs to PIL Image objects
  images = [svg2Image(svgCodeTemplate.format(STROKES=svg)) for svg in svgs]
  images = [addBackgroundImage(i, backgroundImg) for i in images]
  # Create a white rgba background
  grid = imageGrid(images, rows, cols)
  grid.save(filename, "png")

def svg2Image(svg):
  out = io.BytesIO()
  svg2png(bytestring=svg, write_to=out)
  return Image.open(out)

if __name__ == "__main__":
  # output sequences for each char
  args = parser.parse_args()
  mizige.make(ELEM_HEIGHT, ELEM_WIDTH, filename=mizigePath)
  for ch in args.characters: 
    # get json object for character
    strokeMap = getStrokeMap(ch)
    # get list of pngs
    strokeSvgs = getStrokeSvgs(strokeMap)
    # tile images 
    filename = ResultsPath.format(ch=ch, pn=pinyin.get(ch))
    writeStrokePng(strokeSvgs, GRID_COLS,filename)
