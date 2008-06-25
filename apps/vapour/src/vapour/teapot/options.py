class ValidatorOptions:
    
    def __init__(self, htmlVersions = False, defaultResponse = 'rdfxml', validateRdf = False):
        self.htmlVersions = htmlVersions
        self.defaultResponse = defaultResponse
        self.validateRdf = validateRdf
