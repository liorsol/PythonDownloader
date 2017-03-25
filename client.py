# -*- coding: utf-8 -*-
import socket
import errno
import sys
import json
import os


class DownloadClient():

    homepath = os.path.expanduser("~")

    # message = dictionary Object
    def send_msg(self, message):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 6736)
        print >>sys.stderr, 'connecting to %s port %s' % server_address
        try:
            sock.connect(server_address)
        except socket.error as e:
            if e.errno == errno.ECONNREFUSED:
                print >>sys.stderr, "Connection Refused"
                return

        try:
            # Send data
            print >> sys.stderr, 'sending "%s"' % json.dumps(message)
            sock.sendall(json.dumps(message))
            # sock.shutdown(socket.SHUT_WR)
            # retmsg = sock.recv(100)
            # print >> sys.stderr, "Server return msg: %s"%retmsg

        finally:
            print >> sys.stderr, 'closing socket'
            sock.close()


    def download_file(self, url, destfolder):

        message = {'strmsg': 'This is a message', 'command': 'add', 'url': url, 'destfolder': destfolder or self.homepath}
        self.send_msg(message)


    def clear_downloads(self):
        message = {'strmsg': 'This is a message', 'command': 'clear'}
        self.send_msg(message)
