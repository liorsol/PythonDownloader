# -*- coding: utf-8 -*-
import sys

from download import DownloadThread
from Queue import Queue
from server import Server

###
# creates a downloader service listening on IP for dl execution urls
###
class DownloadService(Server):

    def __init__(self, threadNum, port=6736):
        Server.__init__(self, port)
        self.threadNum = threadNum
        self.queue = Queue()
        self.prepare_thread_pool()

    def prepare_thread_pool(self):
        for i in range(self.threadNum):
            t = DownloadThread(self.queue)
            t.start()

    def handle_command(self, msg):
        Server.handle_command(self, msg)
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
