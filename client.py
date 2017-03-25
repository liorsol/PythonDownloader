# -*- coding: utf-8 -*-
import socket
import errno
import sys
import json
import os
import httplib

###
# Creates connection to downloader service
# Sends dl-re service execution commands
# support:
# - add dl url with destination path (optional)
# - Clear pending dls
###
class DownloadClient():

    homepath = os.path.expanduser("~")

    # message = dictionary Object
    def send_msg(self, message):
        # Create a TCP/IP socket
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 6736)
        print >>sys.stderr, 'connecting to %s port %s' % server_address
        try:
            connection.connect(server_address)
        except socket.error as e:
            if e.errno == errno.ECONNREFUSED:
                print >>sys.stderr, "Connection Refused"
                return

        try:
            # Send data
            print >> sys.stderr, 'sending "%s"' % json.dumps(message)
            connection.sendall(json.dumps(message))
            # connection.shutdown(socket.SHUT_WR)
            # retmsg = sock.recv(100)
            # print >> sys.stderr, "Server return msg: %s"%retmsg

        finally:
            print >> sys.stderr, 'closing socket'
            connection.close()

    # Execute url addition for dl to destfolder
    def download_file(self, url, destfolder):
        message = {'command': 'add', 'url': url, 'destfolder': destfolder or self.homepath, 'strmsg': 'This is just a message'}
        self.send_msg(message)

    # Execute clear for all pending dls not in dl status
    def clear_downloads(self):
        message = {'command': 'clear', 'strmsg': 'This is just a message'}
        self.send_msg(message)
