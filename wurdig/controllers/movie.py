import calendar
import datetime as d
import formencode
import logging
import re
import webhelpers.paginate as paginate
import wurdig.lib.helpers as h
import wurdig.model as model
import wurdig.model.meta as meta

from authkit.authorize.pylons_adaptors import authorize
from formencode import htmlfill
from pylons import cache, config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.cache import beaker_cache
from pylons.decorators.rest import restrict
from sqlalchemy.sql import and_, delete
from webhelpers.feedgenerator import Atom1Feed
from wurdig.lib.base import BaseController, Cleanup, ConstructPath, render

log = logging.getLogger(__name__)
from tw.forms.samples import AddUserForm
from tw.mods.pylonshf import validate
from wurdig.model.twforms import *
from pprint import pformat


class MovieController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/movie.mako')
        # or, return a response
        return render('/movie.mako')

    #@h.auth.authorize(h.auth.is_valid_user)
    #@restrict('POST')
    @validate(form=movie_form, error_handler="index")
    def save(self):

        try:
            return pformat(self.form_result)
        except AttributeError:
            return "You must Post, silly!"

        if id is not None:
            movie = db.Movie.get(id)
            if not movie:
                raise Exception('Movie ID not found')
        else:
            movie = db.Movie()
        movie.from_dict(kw)
        
        return "Movie added woot!"
        
    def movie(self, id=None):
        # Return a rendered template
        #return render('/movie.mako')
        # or, return a response
        movie = id is not None and db.Movie.get(id)
        if id is not None and not movie:
            raise Exception('Movie ID not found')
        
        return dict(movie_form=movie_form, movie=movie)
        return render('/movie.mako')
    

