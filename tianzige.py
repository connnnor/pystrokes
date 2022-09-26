import cairo

ELEM_HEIGHT = 1024
ELEM_WIDTH = 1024


OutputPath = "tianzige.png"

def makeTianZiGe(width, height, rgba=(0,0,0,0)):
  
  with cairo.SVGSurface("geek.svg", ELEM_WIDTH, ELEM_HEIGHT) as surface:
  
    # creating a cairo context object
    context = cairo.Context(surface)
    # setting scale of the context
    context.scale(ELEM_HEIGHT, ELEM_WIDTH)
    # setting line width of the context
    (r,g,b,a) = rgba
    context.set_source_rgba(r,g,b,a)
    context.set_line_width(0.01)
    # draw square
    context.move_to(0,0)
    context.line_to(0, 1.0)
    context.line_to(1.0, 1.0)
    context.line_to(1.0, 0)
    context.line_to(0, 0)
    context.stroke()

    # draw horizontal and vertical
    context.set_dash([0.03, 0.01])
    context.set_line_width(0.005)
    context.move_to(0,0.5)
    context.line_to(1.0, 0.5)
    context.move_to(0.5,0)
    context.line_to(0.5, 1.0)
    context.stroke()

    # draw X lines
    context.set_dash([0.03, 0.01])
    context.set_line_width(0.005)
    context.move_to(0,0)
    context.line_to(1.0, 1.0)
    context.stroke()
    context.move_to(0, 1.0)
    context.line_to(1.0, 0)
    context.stroke()
    context.stroke()

    print(f"Writing {OutputPath}")
    surface.write_to_png(OutputPath)
  
if __name__ == "__main__":
  makeTianZiGe(ELEM_HEIGHT - 128, ELEM_WIDTH - 128, rgba=(0.5, 0.01, 0.01, 1.0))

