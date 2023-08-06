import os
import flask
import logging
import socketio
import requests

from bcsdk.impl.sio import sio, set_handler

# disable werkzeug logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = flask.Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    print('Shutting down....')
    shutdown_function = flask.request.environ.get('werkzeug.server.shutdown')
    if shutdown_function is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_function()
    sio.emit('status', {'fill': 'red', 'shape': 'dot',
                        'text': 'Container server down'})
    return 'Server shutting down...'


def _start_server(handler):
    set_handler(handler)
    port = int(os.environ.get('PORT', '3000'))
    print("Starting server on port " + str(port))
    # blocks indefinitely
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)


def _stop_server():
    print('stopping server')
    sio.emit('status', {'fill': 'orange', 'shape': 'dot',
                        'text': 'Shutting down'})
    port = int(os.environ.get('PORT', '3000'))
    requests.post('http://0.0.0.0:{}/shutdown'.format(port))
