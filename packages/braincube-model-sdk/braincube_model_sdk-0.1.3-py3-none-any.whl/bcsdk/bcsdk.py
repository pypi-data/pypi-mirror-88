import logging
import socketio
import flask
import requests
import os

from bcsdk.impl.impl import _start_server, sio, _stop_server


class Handler:
    """
    This class is an abstract class that you should inherit from,
    and implement the on_init, on_destroy and on_message methods.
    """

    def __init__(self):
        global sio
        self.sio = sio

    def on_init(self, conf: dict):
        raise NotImplementedError()

    def on_destroy(self):
        raise NotImplementedError()

    def on_message(self, msg: dict):
        raise NotImplementedError()

    def send_message(self, msg: dict):
        sio.emit('response', msg)


def run_sdk(handler: Handler):
    _start_server(handler)


def stop_sdk():
    _stop_server()


def main():
    print("Starting SDK")
    from bcsdk.examples.mathoperations import MathOperationsHandler
    run_sdk(MathOperationsHandler())


if __name__ == "__main__":
    main()
