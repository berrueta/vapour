import exceptions
import sys

class VapourException(exceptions.Exception):
    """
    Base class for Vapour exceptions.
    """

    def __init__(self):
        Exception.__init__(self)
	
    def __str__(self):
        return ": an exception has occured"

class TooManyRedirections(VapourException):

    def __init__(self, ip):
        VapourException.__init__(self)
        self.ip = str(ip)

    def __str__(self):
        return ": too many redirections, aborting"

class ForbiddenAddress(VapourException):

    def __init__(self, ip):
        VapourException.__init__(self)
        self.ip = str(ip)

    def __str__(self):
        return ": request over %s, internal IP address are forbidden" % self.ip

