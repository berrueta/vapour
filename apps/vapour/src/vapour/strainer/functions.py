import urlparse

def getShortFileName(url):
    parsedUrl = urlparse.urlparse(url) # (protocol,server,path,params,query,fragment)
    newUrl = ("", "", parsedUrl[2], parsedUrl[3], parsedUrl[4], "")
    return urlparse.urlunparse(newUrl)
