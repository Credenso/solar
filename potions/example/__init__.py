from ingredients.bottle import Bottle, route, run, template, view, TEMPLATE_PATH, static_file
import os

app = Bottle()
path = '/base/' # How to get to this module from the root
name = "Example Planet"
description = "This isn't an actual planet, you know."
image_full = f'{path}static/images/full.jpg'
image_thumb = f'{path}static/images/thumb.jpg'

TEMPLATE_PATH.append(f'potions/example/views')

# This handles all the static files in the given system...
# Until we get NGINX to take care of it.
@app.route('/static/<filepath:path>')
def static(filepath):
        return static_file(filepath, root=f'{os.path.dirname(os.path.realpath(__file__))}/static')

@app.route('/')
@view('example/index.tpl')
def index():
    return dict(title="")
