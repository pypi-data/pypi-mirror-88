
import socketio

sio = socketio.Server(async_mode='threading')
current_handler = None


def set_handler(handler):
    global current_handler
    current_handler = handler


@sio.event
def connect(sid, environ):
    print("Edgebox connected")
    sio.emit('status', {'fill': 'green', 'shape': 'dot',
                        'text': 'Edgebox connected'})


@sio.event
def disconnect(sid):
    print("Disconnected")
    current_handler.on_destroy()


@sio.event
def configuration(sid, data):
    print("Received configuration: {}".format(data))
    current_handler.on_init(data)


@sio.event
def msg(sid, data):
    print('Received message ' + str(data))
    current_handler.on_message(data)
