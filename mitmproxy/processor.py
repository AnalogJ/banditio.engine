import time
import os
import json
import pytz
import mitmproxy
from datetime import datetime
from mitmproxy.script import concurrent
from models.entry import Entry
from websocket import create_connection

# """
#     This inline script utilizes harparser.HAR from
#     https://github.com/JustusW/harparser to generate a HAR log object.
# """
# from harparser import HAR



# class _HARLog(HAR.log):
#     # The attributes need to be registered here for them to actually be
#     # available later via self. This is due to HAREncodable linking __getattr__
#     # to __getitem__. Anything that is set only in __init__ will just be added
#     # as key/value pair to self.__classes__.
#     __page_list__ = []
#     __page_count__ = 0
#     __page_ref__ = {}
#
#     def __init__(self, page_list):
#         self.__page_list__ = page_list
#         self.__page_count__ = 0
#         self.__page_ref__ = {}
#
#         HAR.log.__init__(self, {"version": "1.2",
#                                 "creator": {"name": "MITMPROXY HARExtractor",
#                                             "version": "0.1",
#                                             "comment": ""},
#                                 "pages": [],
#                                 "entries": []})
#
#     def reset(self):
#         self.__init__(self.__page_list__)
#
#     def add(self, obj):
#         if isinstance(obj, HAR.pages):
#             self['pages'].append(obj)
#         if isinstance(obj, HAR.entries):
#             self['entries'].append(obj)
#
#     def create_page_id(self):
#         self.__page_count__ += 1
#         return "autopage_%s" % str(self.__page_count__)
#
#     def set_page_ref(self, page, ref):
#         self.__page_ref__[page] = ref
#
#     def get_page_ref(self, page):
#         return self.__page_ref__.get(page, None)
#
#     def get_page_list(self):
#         return self.__page_list__

#
def start(context, argv):
    print("start")
#     """
#         On start we create a HARLog instance. You will have to adapt this to
#         suit your actual needs of HAR generation. As it will probably be
#         necessary to cluster logs by IPs or reset them from time to time.
#     """
#     print "registering parse client"
#     register(os.environ.get('PARSE_CLIENT_KEY'), os.environ.get('PARSE_REST_CLIENT_SECRET'))
#
#     #users should be created by the webapp, but for now, we'll just create the user here.
#     #u = User.signup("dhelmet", "12345")
#     u = User.login(os.environ.get('PARSE_USERNAME'), os.environ.get('PARSE_PASSWORD'))
#     context.user = u
#
#     # context.dump_file = None
#     # if len(argv) > 1:
#     #     context.dump_file = argv[1]
#     # else:
#     #     raise ValueError(
#     #         'Usage: -s "har_extractor.py filename" '
#     #         '(- will output to stdout, filenames ending with .zhar '
#     #         'will result in compressed har)'
#     #     )
#     # context.HARLog = _HARLog(['https://github.com'])
    context.seen_server = set()


def response(context, flow):
    """
       Called when a server response has been received. At the time of this
       message both a request and a response are present and completely done.
    """
    print("response")
    write_to_file('Flow', context)

    # Values are converted from float seconds to int milliseconds later.
    ssl_time = -.001
    connect_time = -.001
    if flow.server_conn not in context.seen_server:
        # Calculate the connect_time for this server_conn. Afterwards add it to
        # seen list, in order to avoid the connect_time being present in entries
        # that use an existing connection.
        connect_time = flow.server_conn.timestamp_tcp_setup - \
                       flow.server_conn.timestamp_start
        context.seen_server.add(flow.server_conn)

        if flow.server_conn.timestamp_ssl_setup is not None:
            # Get the ssl_time for this server_conn as the difference between
            # the start of the successful tcp setup and the successful ssl
            # setup. If  no ssl setup has been made it is left as -1 since it
            # doesn't apply to this connection.
            ssl_time = flow.server_conn.timestamp_ssl_setup - \
                       flow.server_conn.timestamp_tcp_setup

    # Calculate the raw timings from the different timestamps present in the
    # request and response object. For lack of a way to measure it dns timings
    # can not be calculated. The same goes for HAR blocked: MITMProxy will open
    # a server connection as soon as it receives the host and port from the
    # client connection. So the time spent waiting is actually spent waiting
    # between request.timestamp_end and response.timestamp_start thus it
    # correlates to HAR wait instead.
    timings_raw = {
        'send': flow.request.timestamp_end - flow.request.timestamp_start,
        'wait': flow.response.timestamp_start - flow.request.timestamp_end,
        'receive': flow.response.timestamp_end - flow.response.timestamp_start,
        'connect': connect_time,
        'ssl': ssl_time
    }

    # HAR timings are integers in ms, so we have to re-encode the raw timings to
    # that format.
    timings = dict([(key, int(1000 * value))
                    for key, value in timings_raw.iteritems()])

    # The full_time is the sum of all timings. Timings set to -1 will be ignored
    # as per spec.
    full_time = 0
    for item in timings.values():
        if item > -1:
            full_time += item

    started_date_time = datetime.fromtimestamp(
        flow.request.timestamp_start,
        tz=pytz.timezone('UTC')).isoformat()

    request_query_string = [{"name": k, "value": v}
                            for k, v in flow.request.get_query()]
    request_http_version = ".".join([str(v) for v in flow.request.httpversion])
    # Cookies are shaped as tuples by MITMProxy.
    request_cookies = [{"name": k.strip(), "value": v[0]}
                       for k, v in (flow.request.get_cookies() or {}).iteritems()]
    request_headers = [{"name": k, "value": v} for k, v in flow.request.headers]
    request_headers_size = len(str(flow.request.headers))
    request_body_size = len(flow.request.content)

    response_http_version = ".".join(
        [str(v) for v in flow.response.httpversion])
    # Cookies are shaped as tuples by MITMProxy.
    response_cookies = [{"name": k.strip(), "value": v[0]}
                        for k, v in (flow.response.get_cookies() or {}).iteritems()]
    response_headers = [{"name": k, "value": v}
                        for k, v in flow.response.headers]
    response_headers_size = len(str(flow.response.headers))
    response_body_size = len(flow.response.content)
    response_body_decoded_size = len(flow.response.get_decoded_content())
    response_body_compression = response_body_decoded_size - response_body_size
    response_mime_type = flow.response.headers.get_first('Content-Type', '')
    response_redirect_url = flow.response.headers.get_first('Location', '')

    container_id = os.environ['HOSTNAME']

    entry = Entry()
    entry.startedDateTime = started_date_time
    entry.time = full_time
    entry.container_id = container_id
    entry.request = {
        "method": flow.request.method,
        "url": flow.request.url,
        "httpVersion": request_http_version,
        "cookies": request_cookies,
        "headers": request_headers,
        "queryString": request_query_string,
        "headersSize": request_headers_size,
        "bodySize": request_body_size,
    }
    entry.response = {
        "url": flow.request.url,
        "status": flow.response.code,
        "statusText": flow.response.msg,
        "httpVersion": response_http_version,
        "cookies": response_cookies,
        "headers": response_headers,
        "content": {
            "size": response_body_size,
            "compression": response_body_compression,
            "mimeType": response_mime_type},
        "redirectURL": response_redirect_url,
        "headersSize": response_headers_size,
        "bodySize": response_body_size,
    }
    entry.cache = {}
    entry.timings = timings

    #ws = create_connection("ws://localhost:9000/ws/{0}".format(entry.pageref))
    ws = create_connection("ws://websocket.bandit.io:9000/ws/{0}".format(container_id), sslopt={"check_hostname": False})
    ws.send(json.dumps({
        "method": "Network.requestWillBeSent",
        "params": {
            "requestId": "7897.52",
            "frameId": "7897.1",
            "loaderId": "7897.3",
            "documentURL": entry.request['url'],
            "request": {
                "url": entry.request['url'],
                "method": entry.request['method'],
                "headers": {header['name']: header['value'] for header in entry.request['headers']}
            },
            "timestamp": 88986.634829,
            "wallTime": 1440472453.19435,
            "initiator": {"type": "other"},
            "type": "Document"
        }
    }))
    ws.send(json.dumps({
        "method": "Network.responseReceived",
        "params": {
            "requestId": "7897.52",
            "frameId": "7897.1",
            "loaderId": "7897.3",
            "timestamp": 88986.985021,
            "type": "Document",
            "response": {
                "url": entry.response['url'],
                "status": entry.response['status'],
                "statusText": entry.response['statusText'],
                "headers": {header['name']: header['value'] for header in entry.response['headers']},
                "mimeType": entry.response['content']['mimeType'],
                "connectionReused": False,
                "fromDiskCache": False,
                "fromServiceWorker": False,
                "timing": {
                    "requestTime": 88986.636403,
                    "proxyStart": -1,
                    "proxyEnd": -1,
                    "dnsStart": 0,
                    "dnsEnd": 108.372000002419,
                    "connectStart": 108.372000002419,
                    "connectEnd": 113.420000008773,
                    "sslStart": -1,
                    "sslEnd": -1,
                    "serviceWorkerFetchStart": -1,
                    "serviceWorkerFetchReady": -1,
                    "serviceWorkerFetchEnd": -1,
                    "sendStart": 113.492999997106,
                    "sendEnd": 113.573000009637,
                    "receiveHeadersEnd": 347.90900000371
                },
                # "requestHeaders": {
                #     "If-None-Match": "\"1440455137124|#public|0|en|||0\"",
                #     "Accept-Encoding": "gzip, deflate, sdch",
                #     "Host": "www.chromium.org",
                #     "Accept-Language": "en-US,en;q=0.8",
                #     "Upgrade-Insecure-Requests": "1",
                #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
                #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                #     "Cache-Control": "max-age=0",
                #     "Cookie": "_ga=GA1.2.1062414394.1440468745; _gat_SitesTracker=1; __utmt=1; __utma=221884874.1062414394.1440468745.1440468745.1440471278.2; __utmb=221884874.2.10.1440471278; __utmc=221884874; __utmz=221884874.1440468745.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aftzc=QW1lcmljYS9Mb3NfQW5nZWxlczp3eGRhd0FxcWxWZkNYdHRkVVJ2ZStlVEpOOVE9",
                #     "Connection": "keep-alive",
                #     "If-Modified-Since": "Mon, 24 Aug 2015 22:25:37 GMT"
                # },
                "remoteIPAddress": "216.239.32.27",
                "remotePort": 80,
                "protocol": "http/{0}".format(entry.response['httpVersion'])
            }
        }
    }))
    ws.send(json.dumps({
        "method": "Network.dataReceived",
        "params": {
            "requestId": "7897.52",
            "timestamp": 88986.985513,
            "dataLength": entry.response['content']['size'],
            "encodedDataLength": entry.response['bodySize']
        }
    }))
    ws.send(json.dumps({
        "method": "Network.loadingFinished",
        "params": {
            "requestId": "7897.52",
            "timestamp": 88986.985401,
            "encodedDataLength": entry.response['bodySize']
        }
    }))

    #ws.send(json.dumps({"method":"Network.requestWillBeSent","params":{"requestId":"7897.52","frameId":"7897.1","loaderId":"7897.3","documentURL":"http://www.chromium.org/","request":{"url":"http://www.chromium.org/","method":"GET","headers":{"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}},"timestamp":88986.634829,"wallTime":1440472453.19435,"initiator":{"type":"other"},"type":"Document"}}))
    #ws.send(json.dumps({"method":"Network.responseReceived","params":{"requestId":"7897.52","frameId":"7897.1","loaderId":"7897.3","timestamp":88986.985021,"type":"Document","response":{"url":"http://www.chromium.org/","status":304,"statusText":"Not Modified","headers":{"Date":"Tue, 25 Aug 2015 03:14:13 GMT","Last-Modified":"Mon, 24 Aug 2015 22:25:37 GMT","Server":"GSE","X-Robots-Tag":"noarchive","ETag":"\"1440455137124|#public|0|en|||0\""},"mimeType":"text/html","connectionReused":False,"connectionId":2554,"encodedDataLength":-1,"fromDiskCache":False,"fromServiceWorker":False,"timing":{"requestTime":88986.636403,"proxyStart":-1,"proxyEnd":-1,"dnsStart":0,"dnsEnd":108.372000002419,"connectStart":108.372000002419,"connectEnd":113.420000008773,"sslStart":-1,"sslEnd":-1,"serviceWorkerFetchStart":-1,"serviceWorkerFetchReady":-1,"serviceWorkerFetchEnd":-1,"sendStart":113.492999997106,"sendEnd":113.573000009637,"receiveHeadersEnd":347.90900000371},"headersText":"HTTP/1.1 304 Not Modified\r\nX-Robots-Tag: noarchive\r\nLast-Modified: Mon, 24 Aug 2015 22:25:37 GMT\r\nETag: \"1440455137124|#public|0|en|||0\"\r\nDate: Tue, 25 Aug 2015 03:14:13 GMT\r\nServer: GSE\r\n\r\n","requestHeaders":{"If-None-Match":"\"1440455137124|#public|0|en|||0\"","Accept-Encoding":"gzip, deflate, sdch","Host":"www.chromium.org","Accept-Language":"en-US,en;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Cache-Control":"max-age=0","Cookie":"_ga=GA1.2.1062414394.1440468745; _gat_SitesTracker=1; __utmt=1; __utma=221884874.1062414394.1440468745.1440468745.1440471278.2; __utmb=221884874.2.10.1440471278; __utmc=221884874; __utmz=221884874.1440468745.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aftzc=QW1lcmljYS9Mb3NfQW5nZWxlczp3eGRhd0FxcWxWZkNYdHRkVVJ2ZStlVEpOOVE9","Connection":"keep-alive","If-Modified-Since":"Mon, 24 Aug 2015 22:25:37 GMT"},"requestHeadersText":"GET / HTTP/1.1\r\nHost: www.chromium.org\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: en-US,en;q=0.8\r\nCookie: _ga=GA1.2.1062414394.1440468745; _gat_SitesTracker=1; __utmt=1; __utma=221884874.1062414394.1440468745.1440468745.1440471278.2; __utmb=221884874.2.10.1440471278; __utmc=221884874; __utmz=221884874.1440468745.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aftzc=QW1lcmljYS9Mb3NfQW5nZWxlczp3eGRhd0FxcWxWZkNYdHRkVVJ2ZStlVEpOOVE9\r\nIf-None-Match: \"1440455137124|#public|0|en|||0\"\r\nIf-Modified-Since: Mon, 24 Aug 2015 22:25:37 GMT\r\n\r\n","remoteIPAddress":"216.239.32.27","remotePort":80,"protocol":"http/1.1"}}}))
    #ws.send(json.dumps({"method":"Network.dataReceived","params":{"requestId":"7897.52","timestamp":88986.985513,"dataLength":23423,"encodedDataLength":190}}))
    ##WebSocketHandler.ws_send('test', {"method":"Page.frameNavigated","params":{"frame":{"id":"7897.1","loaderId":"7897.3","url":"http://www.chromium.org/","mimeType":"text/html","securityOrigin":"http://www.chromium.org"}}})
    #ws.send(json.dumps({"method":"Network.loadingFinished","params":{"requestId":"7897.52","timestamp":88986.985401,"encodedDataLength":190}}))

    ws.close()


# def done(context):
#     """
#         Called once on script shutdown, after any other events.
#     """
#     from pprint import pprint
#     import json
#
#     json_dump = context.HARLog.json()
#     compressed_json_dump = context.HARLog.compress()
#
#     if context.dump_file == '-':
#         context.log(pprint.pformat(json.loads(json_dump)))
#     elif context.dump_file.endswith('.zhar'):
#         file(context.dump_file, "w").write(compressed_json_dump)
#     else:
#         file(context.dump_file, "w").write(json_dump)
#     context.log(
#         "HAR log finished with %s bytes (%s bytes compressed)" % (
#             len(json_dump), len(compressed_json_dump)
#         )
#     )
#     context.log(
#         "Compression rate is %s%%" % str(
#             100. * len(compressed_json_dump) / len(json_dump)
#         )
#     )
#
#

def write_to_file(title, obj):
    with open("/tmp/debug.txt", "a+") as myfile:
        myfile.write("=================START " + title + "=================\n")
        # myfile.write("\n".join(obj_dump(obj)))
        # myfile.write(json.dumps(obj))
        myfile.write('================= FINISHED ' + title + "=================\n")

def obj_dump(obj):
    obj_attrs = []
    for attr in dir(obj):
        obj_attrs.append("obj.%s = %s" % (attr, getattr(obj, attr)))