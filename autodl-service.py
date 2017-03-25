# -*- coding: utf-8 -*-
import sys
from service import DownloadService

numofthreads = 10
helpstr = """
    [max-tasks-number]
    """
if len(sys.argv) >= 2:
    if sys.argv[1] == '-h':
        print >> sys.stdout, helpstr
        sys.exit()
    if sys.argv[1].isdigit():
        if int(sys.argv[1]) > 0:
            numofthreads = int(sys.argv[1])
ds = DownloadService(numofthreads)
ds.start_listen()
sys.exit()