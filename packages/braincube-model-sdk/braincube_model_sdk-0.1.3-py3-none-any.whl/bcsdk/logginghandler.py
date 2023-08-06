
from bcsdk.bcsdk import Handler


class LoggingHandler(Handler):
    """This handler logs to console everythiong that it received and sends back anything it receives"""

    def on_message(self, msg):
        print("Message received: ", msg)
        self.send_message(msg)

    def on_destroy(self):
        print("Destroyed")

    def on_init(self, conf):
        print("Conf received: ", conf)
