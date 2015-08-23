__author__ = 'jason'
#https://github.com/square/PonyDebugger/blob/master/ponyd/gateway.py
#https://github.com/dpb587/ti-debug/tree/master/lib/dbgp/protocol/inspector/agent
import tornado.options

import tornado
import tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.log
import os
import logging

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print 'new connection'
        self.write_message("connected")

    def on_message(self, message):
        print 'message received %s' % message
        self.write_message('message received %s' % message)

    def on_close(self):
        print 'connection closed'

class Server():

    def __init__(self):
        self.static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'web'))
        self.devtools_path = '/tmp'
        self.listen_port = 8080
        self.listen_interface = '0.0.0.0'

        tornado.options.options.logging = 'debug'
        tornado.log.enable_pretty_logging(options=tornado.options.options)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        application = tornado.web.Application([
            (r"/", MainHandler),
            (r"/ws", WebSocketHandler),
        ])

        print "BanditIo starting. Listening on http://%s:%s" % (self.listen_interface, self.listen_port)

        application.listen(self.listen_port, self.listen_interface)
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.start()


if __name__ == "__main__":
    Server()