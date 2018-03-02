from . import api
from flask import render_template

@api.route('/', methods=['GET'])
def index():
    # example of a route with HTML templating
    message = "Hello, World"
    entries = []
    entries.append({"title":"entry 1", "text":"text 1 ?</>"})
    entries.append({"title":"entry 2", "text":"text 2 ?</>"})
    return render_template('index.html', message=message, entries=entries)

@api.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello, World!'
