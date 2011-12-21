
import urlparse
from dns.resolver import Resolver, NXDOMAIN
from vapour.settings import ALLOW_INTRANET
from vapour.cup import common

def isLocatedAtIntranet(host, options=None):

    logger = common.createLogger()

    logger.debug("security check for host: %s" % host)

    requestFromIntranet = False
    if (options and options.client):
        requestFromIntranet = isIntranet(options.client)

    if (not ALLOW_INTRANET and not requestFromIntranet):
        try:
            resolver = Resolver()
            ipList = resolver.query(host.split(":")[0])
            for ip in ipList:
                if isIntranet(str(ip)):
                    return True, str(ip)
            return False, None
        except NXDOMAIN, e:
            logger.error("%s looks not be a valid hostname: %s" % (host, str(e)))
            return isIntranet(host), host
    else:
        return False, None
            
def isIntranet(ip):
    if ((ip.startswith("192.")) or (ip.startswith("10.")) or (str(ip) is "127.0.0.1")):
        return True
    else:
        return False

def isValidUrl(url):
    parsedUrl = urlparse.urlparse(url)
    if (len(parsedUrl[1])==0 or len(parsedUrl[2])==0):
        return False
    else:
        return True

