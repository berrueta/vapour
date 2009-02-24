defaultUserAgent = "vapour.sourceforge.net"

class ValidatorOptions:
    
    def __init__(self, htmlVersions = False, defaultResponse = 'dontmind', validateRdf = False, userAgent = defaultUserAgent):
        self.htmlVersions = htmlVersions
        self.defaultResponse = defaultResponse
        self.validateRdf = validateRdf
        self.userAgent = userAgent

