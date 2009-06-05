from pylons import g
from webob import Request

def AdminController(environ, start_response):
    req = Request(environ).copy()
    req.path_info_pop() # remove admin prefix
    return g.admin_app(req.environ, start_response)
