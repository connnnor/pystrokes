# pystrokes

This project generates grids showing the stroke order for Chinese characters. 
Many of the apps I've found for learning stroke order display an animation but
I found having a static image more useful.

![](examples/dao_strokes.png)

You can either run a flask server that will display a form where you can input characters and then display the stroke orders on a web page or
you can generate the images locally on the command line

## Sources

__graphics.txt__ stroke data:

* Taken from the [makemeahanzi][1] project which was originally derived from two [Arphic Technology][2] fonts


[1]: https://github.com/skishore/makemeahanzi
[2]: http://www.arphic.com/


## Examples

Web Examples:

![](strokes_screenshot2)
![](strokes_screenshot1.png)
![](form_screenshot.png)


PNG Examples:

![](zhi_strokes.png)
![](dao_strokes.png)
![](le_strokes.png)


## Usage

Starting flask server:

```
$ python3 app.py
usage: app.py [-h] [--host HOST] [--port PORT]

run pystrokes webserver

options:
  -h, --help   show this help message and exit
  --host HOST  flask host
  --port PORT  flask port
```


Generating images locally (this will create 3 images in the `strokes` directory):

```
$ python3 pystrokes.py  知道了
```

