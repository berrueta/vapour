
import urlparse
import dns.resolver
from common import allowIntranet # FIXME: horrible hack, global variable!

def isLocatedAtIntranet(url, options=None):

    parsedUrl = urlparse.urlparse(url) # (_,host,path,_,_,_)
    host = str(parsedUrl[1])
    path = parsedUrl[2]

    requestFromIntranet = False
    if (options and options.client):
        requestFromIntranet = isIntranet(options.client)

    if (not allowIntranet and not requestFromIntranet):
        try:
            ipList = dns.resolver.query(host.split(":")[0])
            for ip in ipList:
                if isIntranet(str(ip)):
                    return True, str(ip)
            return False, None
        except dns.resolver.NXDOMAIN:
            return isIntranet(host), host
    else:
        return False, None
            
def isIntranet(ip):
    if ip.startswith("192.") or ip.startswith("10.") or str(ip) is "127.0.0.1":
        return True
    else:
        return False

