from bcsdk.bcsdk import Handler

import logging

log = logging.getLogger('math example')


class MathOperationsHandler(Handler):
    a = None
    operator = None
    response = None
    operations = {
        'ADD': lambda a, b: a+b,
        'SUB': lambda a, b: a-b,
        'MUL': lambda a, b: a*b,
        'MOD': lambda a, b: a % b,
        'DIV': lambda a, b: a/b
    }

    def __init__(self):
        super().__init__()
        self.operator = self.operations['ADD']

    def on_message(self, msg):
        log.error("on_message: {}".format(msg))
        if self.a is None:
            self.a = int(msg['payload'])
        else:
            response = self.operator(self.a, int(msg['payload']))
            log.error('Emitting response ' + str(response))
            self.send_message(
                {'payload': response})
            self.a = None

    def on_init(self, conf):
        log.error("on_init: {}".format(conf))
        self.operator = self.operations[conf.get('operation', 'ADD')]
        log.error("Operator is " + str(self.operator))

    def on_destroy(self):
        log.error('on_destroy')
