import datetime as d
import formencode
import logging
import re
import wurdig.lib.helpers as h

import wurdig.model as model
import wurdig.model.meta as meta


import webhelpers.paginate as paginate

from authkit.authorize.pylons_adaptors import authorize
from formencode import htmlfill
from pylons import cache, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.cache import beaker_cache
from pylons.decorators.rest import restrict
from sqlalchemy.sql import and_, delete
from wurdig.lib.base import BaseController, Cleanup, ConstructSlug, render

from tw.mods.pylonshf import validate
from wurdig.model.twforms import *
from pprint import pformat

log = logging.getLogger(__name__)
    

class PageController(BaseController):
    
    def view(self, slug=None):
        if slug is None:
            abort(404)
        page_q = Session.query(model.Page)
        c.page = page_q.filter_by(slug=slug).first()
        if c.page is None:
            abort(404)
        if c.page.slug == 'search':
            return render('/derived/page/search.html')
        return render('/derived/page/view.html')

    @h.auth.authorize(h.auth.is_valid_user)
    def new(self):
        return render('/derived/page/new.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewPageForm(), form='new')
    def create(self):
        page = model.Page()
        
        for k, v in self.form_result.items():
            setattr(page, k, v)
            
        page.created_on = d.datetime.now()
        
        meta.Session.add(page)
        meta.Session.commit()
        session['flash'] = 'Page successfully added.'
        session.save()

        return redirect_to(controller='page', 
                           action='view', 
                           slug=page.slug)
    
    @h.auth.authorize(h.auth.is_valid_user)
    def edit(self, id=None):
        if id is None:
            abort(404)
        page_q = meta.Session.query(model.Page)
        page = page_q.filter_by(id=id).first()
        if page is None:
            abort(404)
        values = {
            'id':page.id,
            'title':page.title,
            'slug':page.slug,
            'content':page.content
        }
        return htmlfill.render(render('/derived/page/edit.html'), values)
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewPageForm(), form='edit')
    def save(self, id=None):
        if id is None:
            abort(404)
        page_q = meta.Session.query(model.Page)
        page = page_q.filter_by(id=id).first()
        if page is None:
            abort(404)
            
        for k,v in self.form_result.items():
            if getattr(page, k) != v:
                setattr(page, k, v)
            
        meta.Session.commit()
        session['flash'] = 'Page successfully updated.'
        session.save()

        return redirect_to(controller='page', 
                           action='view', 
                           slug=page.slug)
    
    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        pages_q = meta.Session.query(model.Page)
        c.paginator = paginate.Page(
            pages_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 10,
            controller='page',
            action='list',
        )
        return render('/derived/page/list.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def delete_confirm(self, id=None):
        if id is None:
            abort(404)
        page_q = meta.Session.query(model.Page)
        c.page = page_q.filter_by(id=id).first()
        if c.page is None:
            abort(404)
        return render('/derived/page/delete_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def delete(self, id=None):
        id = request.params.getone('id')
        page_q = meta.Session.query(model.Page)
        page = page_q.filter_by(id=id).first()
        if page is None:
            abort(404)
        meta.Session.delete(page)
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'The page has been deleted'}"
        else:
            session['flash'] = 'Page successfully deleted.'
            session.save()
            return redirect_to(controller='page', action='list')
