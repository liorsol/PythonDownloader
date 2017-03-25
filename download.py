# -*- coding: utf-8 -*-
import sys
import os
import urllib2
import threading
import time

from Queue import Queue

class DownloadThread(threading.Thread):
    def __init__(self, queue):
        print >> sys.stdout, "Creating DownloadThread"
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.daemon = True

    def run(self):
        while True:
            url, destfolder = self.queue.get()
            try:
                self.download_url(url, destfolder)
            except Exception,e:
                print >> sys.stderr, "   Error on trying to download %s: %s"%(url, e)
            self.queue.task_done()

    def download_url(self, url, destfolder):
        dest = self.get_file_destination(url, destfolder)
        print >> sys.stdout, "[%s] Downloading %s -> %s"%(self.ident, url, dest)
        try:
            f = urllib2.urlopen(url)
            with open(dest, "wb") as local_file:
                local_file.write(f.read())
            print >> sys.stdout, "done downloading %s" % (url)
        # handle errors
        except urllib2.HTTPError, e:
            print >> sys.stderr, "downloading %s HTTP Error: %s" % (url, e.code)
        except urllib2.URLError, e:
            print >> sys.stderr, "downloading %s URL Error: %s" % (url, e.reason)

    # returns the file to be created accurding to url and destfolder
    # * if destfolder doesn't exist -> create it
    # * remove trails from url's file name
    # * case file exists -> appending creation number
    def get_file_destination(self, url, destfolder):
        # change it to a different way if you require
        name = url.split('/')[-1].split('?')[0]
        if not os.path.exists(destfolder):
            os.makedirs(destfolder)
        destfile = os.path.join(destfolder, name)
        index = 1
        while os.path.isfile(destfile):
            destfile = os.path.join(destfolder, name + "-" + str(index))
            index += 1
        return destfile


def download(urls, destfolder, numthreads=4):
    queue = Queue()
    for url in urls:
        queue.put((url, destfolder))

    for i in range(numthreads):
        t = DownloadThread(queue)
        t.start()

    time.sleep(10)
    queue.put(("https://en.wikipedia.org/wiki/6", "/tmp/ex1"))
    time.sleep(10)
    queue.put(("https://en.wikipedia.org/wiki/7", "/tmp/ex2"))
    queue.join()

if __name__ == "__main__":
    download(sys.argv[1:], "/tmp")


