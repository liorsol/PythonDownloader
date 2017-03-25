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

    def send_msg(self, message):
        print >> sys.stderr, 'Sending execution message "%s"' % json.dumps(message)

        # get http server ip
        http_server = ('localhost', 6736)
        # create a connection
        conn = httplib.HTTPConnection(*http_server)
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        conn.request("POST", "/", json.dumps(message), headers)

        # get response from server
        rsp = conn.getresponse()

        # print server response and data
        print >> sys.stderr, "Server return status: ", (rsp.status, rsp.reason)
        print >> sys.stderr, "Server return msg: %s" % rsp.read()

        conn.close()

    # Execute url addition for dl to destfolder
    def download_file(self, url, destfolder):
        message = {'command': 'add', 'url': url, 'destfolder': destfolder or self.homepath, 'strmsg': 'This is just a message'}
        self.send_msg(message)

    # Execute clear for all pending dls not in dl status
    def clear_downloads(self):
        message = {'command': 'clear', 'strmsg': 'This is just a message'}
        self.send_msg(message)
