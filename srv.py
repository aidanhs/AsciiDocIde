
import os
import json
import bottle
from bottle import route, request, response, static_file

DIR = os.path.dirname(os.path.abspath(__file__))

@route('/_ide/save', method='POST')
def save():
    path = request.json['path']
    data = request.json['data']
    open(path, 'w').write(data.encode('utf-8'))
    return '""'

@route('/_ide/load', method='GET')
def load():
    return json.dumps(
        open(os.path.join('.', request.GET.path)).read().decode('utf-8'),
        encoding='utf-8'
    )

@route('/_ide/filelist', method='GET')
def filelist():
    files = []
    for root, dirnames, filenames in os.walk('.'):
        if '.git' in dirnames:
            dirnames.remove('.git')
        for filename in filenames:
            files.append(os.path.join(root, filename))
    assert all([f.startswith('./') for f in files])
    files = [f[2:] for f in files]
    files.sort()
    return json.dumps(files)

@route('/')
def index():
    return static_file('index.html', root=DIR)
@route('/_ide/static/AsciiDocBox/<path:path>')
def static_srv(path):
    return static_file(path, root=os.path.join(DIR, 'AsciiDocBox'))
@route('/_ide/static/<path:path>.js')
def static_srv2(path):
    return static_file(path + '.js', root=DIR)
@route('<path:path>')
def static_srv3(path):
    return static_file(path, root='.')

@route('/export/<fname>.doc')
def export_doc(fname):
    pass

def start():
    # Start the server
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 8001))
    bottle.debug(True)
    bottle.run(host=host, port=port)

if __name__ == '__main__':
    start()
