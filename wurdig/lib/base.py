"""The base Controller API

Provides the BaseController class for subclassing.
"""
import formencode
import re
import wurdig.lib.helpers as h

from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from wurdig.model import Session
import wurdig.model as model

class Cleanup(formencode.FancyValidator):
    def _to_python(self, value, state):
        if value['content'] not in ['', u'', None]:
            value['content'] = h.mytidy(value['content'])
        return value
    
class ConstructSlug(formencode.FancyValidator):
    def _to_python(self, value, state):
        if value['slug'] in ['', u'', None]:
            title = value['title'].lower()
            value['slug'] = re.compile(r'[^\w-]+', re.U).sub('-', title).strip('-')
        return value

class BaseController(WSGIController):     
    
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()
