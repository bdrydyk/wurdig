from pylons import config
from paste.deploy.converters import asbool
from wurdig.model import meta
import os
import wurdig.model as model

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """
    def __init__(self):
        """One instance of Globals is created during application

          initialization and is available during requests via the
        'app_globals' variable

        """


