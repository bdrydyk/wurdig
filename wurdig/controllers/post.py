import calendar
import datetime as d
import formencode
import logging
import re
import webhelpers.paginate as paginate
import wurdig.lib.helpers as h


import wurdig.model as model
import wurdig.model.meta as meta
from wurdig.model import *

from authkit.authorize.pylons_adaptors import authorize
from formencode import htmlfill
from pylons import cache, config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.cache import beaker_cache
from pylons.decorators.rest import restrict
from sqlalchemy.sql import and_, delete
from webhelpers.feedgenerator import Atom1Feed
from wurdig.lib.base import BaseController, Cleanup, ConstructSlug, render

from wurdig.model.twforms import *

from authkit.permissions import ValidAuthKitUser
from authkit.authorize.pylons_adaptors import authorize

log = logging.getLogger(__name__)



class PostController(BaseController):
    
    def home(self):
        posts_q = Session.query(model.Post).filter(
            model.Post.draft == False
        )
        c.paginator = paginate.Page(
            posts_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 10,
            controller='post',
            action='home'
        )
        return render('/derived/post/home.html')
    
    def redirect_wp_feeds(self):
        return redirect_to(controller='post', action='feeds', _code=301)
        
    @beaker_cache(expire=28800, type='memory', cache_key='post_feeds')
    def feeds(self):
        item_tag_table = metadata.tables['item_tag']
        posts_q = Session.query(Post).filter(
            Post.draft == False
        ).order_by([Post.posted_on.desc()]).limit(10)
        
        feed = Atom1Feed(
            title=config['blog.title'],
            subtitle=config['blog.subtitle'],
            link=u"http://%s" % request.server_name,
            description=u"Most recent posts for %s" % config['blog.title'],
            language=u"en",
        )
        
        for post in posts_q:
            feed.add_item(
                title=post.title,
                link=u'http://%s%s' % (request.server_name, h.url_for(
                    controller='post', 
                    action='view', 
                    year=post.posted_on.strftime('%Y'), 
                    month=post.posted_on.strftime('%m'), 
                    slug=post.slug
                )),
                description=post.content,
                categories=tuple(post.tags)
            )
                
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
    
    def archive(self, year=None, month=None):   
        if year is None:
            abort(404)
        
        (c.date, year_i, month_start, month_end, day_end) = (year, int(year), 1, 12, 31)
        
        if month is not None:
            c.date = calendar.month_name[month_start] + ', ' + year
            (month_start, month_end) = (int(month), int(month))
            day_end = calendar.monthrange(year_i, month_start)[1]
        
        posts_q = meta.Session.query(model.Post).filter(
            and_(
                model.Post.posted_on >= d.datetime(year_i, month_start, 1), 
                model.Post.posted_on <= d.datetime(year_i, month_end, day_end), 
                model.Post.draft == False
            )
        )
        
        c.paginator = paginate.Page(
            posts_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 10,
            controller='post',
            action='archive',
            year=year,
            month=month,
        )
                
        return render('/derived/post/archive.html')
    
    def view(self, year, month, slug):
        (year_i, month_i) = (int(year), int(month))
        
        post_tag_table = metadata.tables['post_tag']
        
        c.post = meta.Session.query(model.Post).filter(
            and_(model.Post.posted_on >= d.datetime(year_i, month_i, 1), 
                 model.Post.posted_on <= d.datetime(year_i, month_i, calendar.monthrange(year_i, month_i)[1]),
                 model.Post.draft == False,
                 model.Post.slug == slug)
        ).first()
                                 
        if c.post is None:
            abort(404)
            
        return render('/derived/post/view.html')
    
    @authorize(ValidAuthKitUser())
    def new(self):
        tag_q = meta.Session.query(model.Tag)
        c.available_tags = [(tag.id, tag.name) for tag in tag_q]
        return render('/derived/post/new.html')
    
    @authorize(ValidAuthKitUser())
    @restrict('POST')
    @validate(schema=NewPostForm(), form='new')
    def create(self):
        post = model.Post()
        
        tags = self.form_result['tags']
        del self.form_result['tags']
        
        for k, v in self.form_result.items():
            setattr(post, k, v)
        
        if not post.draft:
            post.posted_on = d.datetime.now()
        
        post.created_on = d.datetime.now()
        
        meta.Session.add(post)

        for tag in tags:
            t = meta.Session.query(model.Tag).get(tag)
            post.tags.append(t)
        
        meta.Session.commit()        
        session['flash'] = 'Post successfully added.'
        session.save()
        # Issue an HTTP redirect
        if post.posted_on is not None:
            return redirect_to(controller='post', 
                               action='view', 
                               year=post.posted_on.strftime('%Y'), 
                               month=post.posted_on.strftime('%m'), 
                               slug=post.slug)
        else:
            return redirect_to(controller='post', action='list')
    
    @authorize(ValidAuthKitUser())
    def edit(self, id=None):
        if id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = post_q.filter_by(id=id).first()
        if c.post is None:
            abort(404)
        import pprint
        
        tag_q = meta.Session.query(model.Tag)
        c.available_tags = [(tag.id, tag.name) for tag in tag_q]
        c.selected_tags = [str(tag.id) for tag in c.post.tags]
        
        values = {
            'id':c.post.id,
            'title':c.post.title,
            'slug':c.post.slug,
            'content':c.post.content,
            'draft':c.post.draft,
            'comments_allowed':c.post.comments_allowed,
            'tags':c.selected_tags
        }
        return htmlfill.render(render('/derived/post/edit.html'), values)
    
    @authorize(ValidAuthKitUser())
    @restrict('POST')
    @validate(schema=NewPostForm(), form='edit')
    def save(self, id=None):
        if id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        post = post_q.filter_by(id=id).first()
        if post is None:
            abort(404)
            
        posted_tags = self.form_result['tags']
        del self.form_result['tags']
            
        for k,v in self.form_result.items():
            if getattr(post, k) != v:
                setattr(post, k, v)
                
        # is this post marked draft or not
        if post.draft:
            post.posted_on = None
        elif post.posted_on is None:
            post.posted_on = d.datetime.now()
        
        # remove existing tags which were not selected
        # in the "posted" tags
        for i, tag in enumerate(post.tags):
            if tag.id not in posted_tags:
                del post.tags[i]
        
        # let's add the new tags for this post
        tagids = [tag.id for tag in post.tags]
        for tag in posted_tags:
            if tag not in tagids:
                t = meta.Session.query(model.Tag).get(tag)
                post.tags.append(t)
            
        meta.Session.commit()
        session['flash'] = 'Post successfully updated.'
        session.save()

        if not post.draft:
            return redirect_to(controller='post', 
                               action='view', 
                               year=post.posted_on.strftime('%Y'), 
                               month=post.posted_on.strftime('%m'), 
                               slug=post.slug)
        else:
            return redirect_to(controller='post', action='list')
    
    @authorize(ValidAuthKitUser())
    def list(self):
        posts_q = meta.Session.query(model.Post).order_by([model.Post.draft.desc(),model.Post.posted_on.desc()])
        c.paginator = paginate.Page(
            posts_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 50,
            controller='post',
            action='list',
        )
        return render('/derived/post/list.html')
    
    @authorize(ValidAuthKitUser())
    def delete_confirm(self, id=None):
        if id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = post_q.filter_by(id=id).first()
        if c.post is None:
            abort(404)
        return render('/derived/post/delete_confirm.html')

    @authorize(ValidAuthKitUser())
    @restrict('POST')
    def delete(self, id=None):
        id = request.params.getone('id')
        post_q = meta.Session.query(model.Post)
        post = post_q.filter_by(id=id).first()
        if post is None:
            abort(404)
        # delete tags and comments associated with post
        meta.Session.execute(delete(model.poststags_table, model.poststags_table.c.post_id==post.id))
        meta.Session.execute(delete(model.comments_table, model.comments_table.c.post_id==post.id))
        meta.Session.delete(post)
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'The post has been deleted'}"
        else:
            session['flash'] = 'Post successfully deleted.'
            session.save()
            return redirect_to(controller='post', action='list')

    def form(self, id=None):
        """docstring for form"""
        
        return render('/movie.mako')