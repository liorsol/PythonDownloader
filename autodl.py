# -*- coding: utf-8 -*-
import sys
from client import DownloadClient

helpstr = """
add <url> [path]    Add the URL to the service to download.
                    If path is not given, the current user’s home directory is used instead.
clear               The service will finish its ongoing tasks and not start new ones.
                    All the previously added URLs should be forgotten.
"""
dc = DownloadClient()
if len(sys.argv) >= 2:
    if sys.argv[1] == '-h':
        print >> sys.stdout, helpstr
        sys.exit()
    elif sys.argv[1] == 'clear':
        dc.clear_downloads()
        sys.exit()
    elif len(sys.argv) >= 3:
        if sys.argv[1] == 'add':
            dc.download_file(sys.argv[2], (sys.argv[3:4] or (False,))[0])
            sys.exit()
print >> sys.stdout, "unknown command, -h for more help"
sys.exit()