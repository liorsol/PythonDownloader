# -*- coding: utf-8 -*-
import socket
import sys
import json

from download import DownloadThread
from Queue import Queue

class DownloadService():

    PORT = 6736

    def __init__(self, threadNum, port=6736):
        self.threadNum = threadNum
        self.PORT = port
        self.queue = Queue()
        self.prepareThreadPool()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.create_socket()

    def prepareThreadPool(self):
        for i in range(self.threadNum):
            t = DownloadThread(self.queue)
            t.start()

    def create_socket(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the port
        server_address = ('localhost', self.PORT)
        print >>sys.stdout, 'starting up on %s port %s' % server_address
        self.sock.bind(server_address)

    def start_listen(self):
        # Listen for incoming connections
        self.sock.listen(1)

        while True:
            # Wait for a connection
            print >>sys.stderr, 'waiting for a connection'
            connection, client_address = self.sock.accept()
            data = ""
            try:
                print >>sys.stdout, 'connection from', client_address
                retmsg = ""
                while True:
                    datatmp = connection.recv(100)
                    if not datatmp:
                        break
                    data += datatmp
                retmsg = self.handle_command(json.loads(data))

                # self.sock.sendall(retmsg)


            finally:
                # Clean up the connection
                print >> sys.stderr, "closing connection"
                connection.close()

    def handle_command(self, msg):
        print >> sys.stdout, 'received "%s"' % json.dumps(msg)
        if msg.has_key('command'):
            if msg.get('command') == 'add':
                return self.download_file(msg)
            elif msg.get('command') == 'clear':
                return self.clear_waiting_downloads()
        return "Unknown command"

    def download_file(self, msg):
        if msg.has_key('url'):
            print >> sys.stdout, 'url "%s"' % msg['url']
            self.queue.put((msg['url'], msg.get('destfolder', '/tmp')))
            return "Url was added for download"
        return "Url to download not found"

    def clear_waiting_downloads(self):
        print >> sys.stdout, 'Clearing download waiting queue'
        while not self.queue.empty():
            self.queue.get()
        return "Clear queue done"
