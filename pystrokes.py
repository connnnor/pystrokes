import sys
import json
from cairosvg import svg2png
from PIL import Image
import math
import io
import pinyin

WRITE_EVERY_STROKE = False

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
BackgroundPath = './tianzige.png'

# keys = character, strokes, medians
strokeMap = {}

def getStrokeMap(character):
  with open(GraphicsPath, "r") as f:
    for line in f:
      if character in line:
        return json.loads(line)
    return None

def getStrokePngs(strokeMap):
  strokes = strokeMap["strokes"]
  print(f'len(strokes) = {len(strokes)}')
  strokesPng = [] 
  for i in range(0, len(strokes)+1):
    svgPaths = []
    for j in range(0, i):
      if j == i-1:
        color = "#FF0000" # red
      else:
        color = "#000000" # black
      svgPaths.append(svgPathTemplate.format(COLOR=color,DATA=strokes[j]))
    svgCode = svgCodeTemplate.format(STROKES="\n".join(svgPaths))
    strokesPng.append(svg2png(bytestring=svgCode,write_to=None))
    if WRITE_EVERY_STROKE:
      svg2png(bytestring=svgCode,write_to=f"stroke_{i:02d}.png")
  return strokesPng

def tilePngs(pngs, nCols, elemHeight, elemWidth):
  print(f'len(pngs) = {len(pngs)}')
  numRows = math.ceil(len(pngs) / nCols)
  imgWidth = ELEM_WIDTH * GRID_COLS
  imgHeight = ELEM_HEIGHT * numRows
  newImg = Image.new('RGBA', (imgWidth, imgHeight),color=(255,255,255,0))
  print(f"Dimensions: W x H = {imgWidth} x {imgHeight}")
  for i, png in enumerate(pngs):
    backImg = Image.open(BackgroundPath)
    backFill = Image.new("RGBA", (ELEM_WIDTH, ELEM_HEIGHT), "WHITE") # Create a white rgba background
    strokeImg = Image.open(io.BytesIO(png))
    xPos = (i % nCols) * ELEM_WIDTH
    yPos = (i // nCols) * ELEM_HEIGHT
    print(f"Pasting stroke[{i}] at {xPos} x {yPos}")
    backFill.alpha_composite(backImg, (0, 0))
    newImg.paste(backFill, (xPos, yPos))
    newImg.alpha_composite(strokeImg, (xPos, yPos))
  imgByteArr = io.BytesIO()
  newImg.save(imgByteArr, "png")
  return imgByteArr.getvalue()

if __name__ == "__main__":
  # output sequences for each char
  character = sys.argv[1]
  # get json object for character
  strokeMap = getStrokeMap(character)
  # get list of pngs
  strokePngs = getStrokePngs(strokeMap)
  # tile images 
  pngBytes = tilePngs(strokePngs[1:], GRID_COLS, ELEM_HEIGHT, ELEM_WIDTH)
  filename = ResultsPath.format(ch=character, pn=pinyin.get(character))
  with open(filename, "wb") as f:
      print(f"writing {f.name}")
      f.write(pngBytes)
   
