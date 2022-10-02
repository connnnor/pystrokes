from cairosvg import svg2png

ELEM_HEIGHT = 1024
ELEM_WIDTH = 1024

SVG_CODE_TEMPLATE = """
<svg viewBox="0 0 1024 1024" style="fill">
    <!-- tianzige guidelines -->
    <svg style="stroke:{strokeColor};stroke-width: 5;fill-opacity:0.0;stroke-opacity:1;">
      <g transform="scale(1, 1)">
        <line x1="0" y1="512" x2="1024" y2="512" stroke-dasharray="32 16"/>
        <line x1="512" y1="0" x2="512" y2="1024" stroke-dasharray="32 16"/>
        <line x1="0" y1="0" x2="1024" y2="1024" stroke-dasharray="32 16"/>
        <line x1="0" y1="1024" x2="1024" y2="0" stroke-dasharray="32 16"/>
        <rect x="0" y="0" width="1020" height="1020"/>
      </g>
    </svg>
</svg>
"""

def make(width, height, filename, strokeColor="darkred"):
  svg2png(bytestring=SVG_CODE_TEMPLATE.format(strokeColor=strokeColor),
          write_to=filename,
          output_width=width,
          output_height=height)

if __name__ == "__main__":
  make(ELEM_HEIGHT, ELEM_WIDTH, filename="mizige.png")
