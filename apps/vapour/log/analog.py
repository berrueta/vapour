#!/usr/bin/python
# -*- coding: utf-8 -

# A tool to analyze logs produced by Vapour
# 
# Copyright (c) 2008 Sergio Fernández <sergio.fernandez@fundacionctic.org>
#
# This file is part of Vapour <http://vapour.sf.net/>

import sys
import urlparse
from operator import itemgetter

class AnaLog:

    def __init__(self, path):
        self.path = path
        self.stats = Stats()

    def analyze(self):
        for line in open(self.path, "r"):
            uri = line[:-1].split(" ")[-1]
            if (uri.startswith("http://")):
                self.addRequest(uri)

    def addRequest(self, uri):
        host = urlparse.urlparse(uri)[1] # (protocol,host,path,_,_,_)
        self.stats.addHostRequest(host.split(":")[0])

    def __str__(self):
        return str(self.stats)

class Stats:

    def __init__(self):
        self.hosts = {}

    def addHostRequest(self, host):
        if (len(host.split("."))>1):
            if self.hosts.has_key(host):
                self.hosts[host] += 1
            else:
                self.hosts[host] = 1

    def __str__(self):
        string = ""
        for host, count in sorted(self.hosts.iteritems(), key=itemgetter(1), reverse=True):
            string += "%s,%i\n" % (host, count)
        return string


def usage():
    print """
    Usage:
        python analog.py <vapour.log>

    """
    sys.exit(-1)


if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        if (len(args)<1):
            usage()
        else:
            al = AnaLog(args[0])
            al.analyze()
            print al
    except KeyboardInterrupt:
        print "Received Ctrl+C or another break signal. Exiting..."

