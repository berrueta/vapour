import exceptions
import sys

class VapourException(exceptions.Exception):
    """
    Base class for Vapour exceptions.
    """

    def __init__(self):
        Exception.__init__(self)
	
    def __str__(self):
        return "VapourException: an exception has occured"

class TooManyRedirections(VapourException):
    """
    Too many redirections exception
    """

    def __init__(self, ip):
        VapourException.__init__(self)
        self.ip = str(ip)

    def __str__(self):
        return "TooManyRedirections: too many redirections, aborting"

class ForbiddenAddress(VapourException):
    """
    Forbidden address exception
    """

    def __init__(self, ip, url):
        VapourException.__init__(self)
        self.ip = ip
        self.url = url

    def __str__(self):
        return "ForbiddenAddress: forbidden request to %s (resolves to IP %s), internal IP addresses are forbidden" % (self.url, str(self.ip))

class IlegalLocationValue(VapourException):
    """
    Ilegal location value exception
    """

    def __init__(self, value):
        VapourException.__init__(self)
        self.value = value

    def __str__(self):
        return "IlegalLocationValue: the value of the location header in the response (%s) is not an absolute URI (see section 14.30 in RFC2616)" % self.value

