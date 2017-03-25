from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sys
import json

class DownloaderHTTPRequestHandler(BaseHTTPRequestHandler):
    # handle GET command
    def do_POST(self):
        try:
            print >> sys.stdout, 'New connection with message...'

            # send header first
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            post_data = self.rfile.read(int(self.headers['Content-Length']))
            # retmsg = self.handle_command(json.loads(post_data))
            # send response
            # send code 200 response
            self.send_response(200)
            self.wfile.write(json.dumps('{"aa":11}'))
            print post_data
            print >> sys.stdout, "closing connection"
            return

        except IOError:
            self.send_error(404, 'Error on trying to add download')

class DownloaderHTTP():

    PORT = 6736

    def __init__(self, port=6736):
        #super(DownloaderHTTP, self).__init__()
        self.PORT = port
        self.create_listener()
        self.start_listen()

    def do_POST(self):
        try:
            print >> sys.stdout, 'New connection with message...'

            # send header first
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            post_data = self.rfile.read(int(self.headers['Content-Length']))
            # retmsg = self.handle_command(json.loads(post_data))
            # send response
            # send code 200 response
            self.send_response(200)
            self.wfile.write(json.dumps('{"aa":11}'))
            print post_data
            print >> sys.stdout, "closing connection"
            return

        except IOError:
            self.send_error(404, 'Error on trying to add download')

    def create_listener(self):
        server_address = ('localhost', self.PORT)
        self.httpd = HTTPServer(server_address, DownloaderHTTPRequestHandler)
        print >> sys.stdout, 'Starting up http server on %s port %s' % server_address

    def start_listen(self):
        print >> sys.stderr, 'waiting for a connection'
        self.httpd.serve_forever()

    def handle_command(self, msg):
        print >> sys.stdout, 'received "%s"' % json.dumps(msg)
        return "Unknown command"


def run():
    print('http server is starting...')

    # ip and port of servr
    # by default http server port is 80
    server_address = ('127.0.0.1', 6736)
    httpd = HTTPServer(server_address, DownloaderHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()


if __name__ == '__main__':
    # run()
    s = DownloaderHTTP()
    s.start_listen()