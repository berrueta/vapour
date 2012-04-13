
import logging
from vapour.settings import DEBUG

def getLogger(name="vapour"):
    if DEBUG:
        name = name + ".dev"
    return logging.getLogger(name)
