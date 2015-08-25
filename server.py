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
import json
from agent.console import Console
from agent.debugger import Debugger
from agent.dom import Dom
from agent.dom_debugger import DomDebugger
from agent.input import Input
from agent.network import Network
from agent.page import Page
from agent.runtime import Runtime
from agent.timeline import Timeline

from parse_rest.connection import register,SessionToken
from parse_rest.user import User
from parse_rest.datatypes import ACL


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        WebSocketHandler.ws_send('test',{"method":"Network.responseReceived","params":{"requestId":"7897.16","frameId":"7897.1","loaderId":"7897.2","timestamp":87808.405844,"type":"Other","response":{"url":"http://www.chromium.org/","status":200,"statusText":"OK","headers":{"Date":"Tue, 25 Aug 2015 02:12:24 GMT","Content-Encoding":"gzip","X-Content-Type-Options":"nosniff","Last-Modified":"Mon, 24 Aug 2015 22:25:37 GMT","Server":"GSE","Age":"0","ETag":"\"1440455137124|#public|0|en|||0\"","X-Frame-Options":"SAMEORIGIN","Content-Type":"text/html; charset=utf-8","Cache-Control":"public, max-age=5","X-Robots-Tag":"noarchive","Content-Length":"6810","X-XSS-Protection":"1; mode=block","Expires":"Tue, 25 Aug 2015 01:31:23 GMT"},"mimeType":"text/html","connectionReused":False,"connectionId":0,"encodedDataLength":-1,"fromDiskCache":True,"fromServiceWorker":False,"timing":{"requestTime":87808.405171,"proxyStart":-1,"proxyEnd":-1,"dnsStart":-1,"dnsEnd":-1,"connectStart":-1,"connectEnd":-1,"sslStart":-1,"sslEnd":-1,"serviceWorkerFetchStart":-1,"serviceWorkerFetchReady":-1,"serviceWorkerFetchEnd":-1,"sendStart":0.218000001041219,"sendEnd":0.218000001041219,"receiveHeadersEnd":0.409999993280508},"remoteIPAddress":"216.239.32.27","remotePort":80,"protocol":"http/1.1"}}})
        WebSocketHandler.ws_send('test', {"method":"Network.dataReceived","params":{"requestId":"7897.16","timestamp":87808.406327,"dataLength":23423,"encodedDataLength":0}})
        WebSocketHandler.ws_send('test', {"method":"Network.loadingFinished","params":{"requestId":"7897.16","timestamp":87808.406273,"encodedDataLength":0}})
        WebSocketHandler.ws_send('test', {"method":"Page.frameStartedLoading","params":{"frameId":"7897.1"}})
        WebSocketHandler.ws_send('test', {"method":"Network.requestWillBeSent","params":{"requestId":"7897.52","frameId":"7897.1","loaderId":"7897.3","documentURL":"http://www.chromium.org/","request":{"url":"http://www.chromium.org/","method":"GET","headers":{"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}},"timestamp":88986.634829,"wallTime":1440472453.19435,"initiator":{"type":"other"},"type":"Document"}})
        WebSocketHandler.ws_send('test', {"method":"Network.responseReceived","params":{"requestId":"7897.52","frameId":"7897.1","loaderId":"7897.3","timestamp":88986.985021,"type":"Document","response":{"url":"http://www.chromium.org/","status":304,"statusText":"Not Modified","headers":{"Date":"Tue, 25 Aug 2015 03:14:13 GMT","Last-Modified":"Mon, 24 Aug 2015 22:25:37 GMT","Server":"GSE","X-Robots-Tag":"noarchive","ETag":"\"1440455137124|#public|0|en|||0\""},"mimeType":"text/html","connectionReused":False,"connectionId":2554,"encodedDataLength":-1,"fromDiskCache":False,"fromServiceWorker":False,"timing":{"requestTime":88986.636403,"proxyStart":-1,"proxyEnd":-1,"dnsStart":0,"dnsEnd":108.372000002419,"connectStart":108.372000002419,"connectEnd":113.420000008773,"sslStart":-1,"sslEnd":-1,"serviceWorkerFetchStart":-1,"serviceWorkerFetchReady":-1,"serviceWorkerFetchEnd":-1,"sendStart":113.492999997106,"sendEnd":113.573000009637,"receiveHeadersEnd":347.90900000371},"headersText":"HTTP/1.1 304 Not Modified\r\nX-Robots-Tag: noarchive\r\nLast-Modified: Mon, 24 Aug 2015 22:25:37 GMT\r\nETag: \"1440455137124|#public|0|en|||0\"\r\nDate: Tue, 25 Aug 2015 03:14:13 GMT\r\nServer: GSE\r\n\r\n","requestHeaders":{"If-None-Match":"\"1440455137124|#public|0|en|||0\"","Accept-Encoding":"gzip, deflate, sdch","Host":"www.chromium.org","Accept-Language":"en-US,en;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Cache-Control":"max-age=0","Cookie":"_ga=GA1.2.1062414394.1440468745; _gat_SitesTracker=1; __utmt=1; __utma=221884874.1062414394.1440468745.1440468745.1440471278.2; __utmb=221884874.2.10.1440471278; __utmc=221884874; __utmz=221884874.1440468745.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aftzc=QW1lcmljYS9Mb3NfQW5nZWxlczp3eGRhd0FxcWxWZkNYdHRkVVJ2ZStlVEpOOVE9","Connection":"keep-alive","If-Modified-Since":"Mon, 24 Aug 2015 22:25:37 GMT"},"requestHeadersText":"GET / HTTP/1.1\r\nHost: www.chromium.org\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: en-US,en;q=0.8\r\nCookie: _ga=GA1.2.1062414394.1440468745; _gat_SitesTracker=1; __utmt=1; __utma=221884874.1062414394.1440468745.1440468745.1440471278.2; __utmb=221884874.2.10.1440471278; __utmc=221884874; __utmz=221884874.1440468745.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aftzc=QW1lcmljYS9Mb3NfQW5nZWxlczp3eGRhd0FxcWxWZkNYdHRkVVJ2ZStlVEpOOVE9\r\nIf-None-Match: \"1440455137124|#public|0|en|||0\"\r\nIf-Modified-Since: Mon, 24 Aug 2015 22:25:37 GMT\r\n\r\n","remoteIPAddress":"216.239.32.27","remotePort":80,"protocol":"http/1.1"}}})
        WebSocketHandler.ws_send('test', {"method":"Network.dataReceived","params":{"requestId":"7897.52","timestamp":88986.985513,"dataLength":23423,"encodedDataLength":190}})
        WebSocketHandler.ws_send('test', {"method":"Page.frameNavigated","params":{"frame":{"id":"7897.1","loaderId":"7897.3","url":"http://www.chromium.org/","mimeType":"text/html","securityOrigin":"http://www.chromium.org"}}})
        WebSocketHandler.ws_send('test', {"method":"Network.loadingFinished","params":{"requestId":"7897.52","timestamp":88986.985401,"encodedDataLength":190}})
        WebSocketHandler.ws_send('test', {"method":"Page.loadEventFired","params":{"timestamp":88987.121584}})
        WebSocketHandler.ws_send('test', {"method":"Page.frameStoppedLoading","params":{"frameId":"7897.1"}})

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    sockets = {}
    def check_origin(self, origin):
        return True

    def open(self, page_id):
        print 'new connection'
        self.page_id = page_id
        #u = User.signup("dhelmet", "12345")
        self.user = User.login(os.environ.get('PARSE_USERNAME'), os.environ.get('PARSE_PASSWORD'))
        WebSocketHandler.sockets[page_id] = self
        self.write_message("connected")

    def on_message(self, message):
        print 'message received %s' % message
        payload = json.loads(message)

        type, method = payload['method'].split('.')
        response = {}
        try:
            if type == 'Console':
                response = getattr(Console, method)()
            elif type == 'Debugger':
                response = getattr(Debugger, method)()
            elif type == 'DOM':
                response = getattr(Dom, method)()
            elif type == 'DOMDebugger':
                response = getattr(DomDebugger, method)()
            elif type == 'Input':
                response = getattr(Input, method)()
            elif type == 'Network':
                response = getattr(Network, method)()
            elif type == 'Page':
                response = getattr(Page, method)()
            elif type == 'Runtime':
                response = getattr(Runtime, method)()
            elif type == 'Timeline':
                response = getattr(Timeline, method)()
            else:
                response = {"error":"Unimplemented"}
        except:
            response = {"error":"Unimplemented Method"}

        response['id'] = payload['id']
        print response
        self.write_message(response)

    def on_close(self):
        print 'connection closed'

    @classmethod
    def ws_send(cls, socket_id, message):
        socket = cls.sockets[socket_id]

        if not socket.ws_connection.stream.socket:
            print "Web socket does not exist anymore!!!"
            del cls.sockets[socket_id]
        else:
            socket.write_message(message)

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
            (r"/ws/(.*)", WebSocketHandler),
        ])

        print "BanditIo starting. Listening on http://%s:%s" % (self.listen_interface, self.listen_port)

        application.listen(self.listen_port, self.listen_interface)
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.start()


if __name__ == "__main__":
    register(os.environ.get('PARSE_CLIENT_KEY'), os.environ.get('PARSE_REST_CLIENT_SECRET'))

    Server()

    print "this happens after the loops tarts"