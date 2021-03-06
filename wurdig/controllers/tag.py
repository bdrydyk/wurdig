import datetime as d
import formencode
import logging
import re
import wurdig.model as model
import wurdig.model.meta as meta
import wurdig.lib.helpers as h
import webhelpers.paginate as paginate

from authkit.authorize.pylons_adaptors import authorize
from formencode import htmlfill
from pylons import cache, config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.cache import beaker_cache
from pylons.decorators.rest import restrict
from sqlalchemy import func
from sqlalchemy.sql import and_, delete
from webhelpers.feedgenerator import Atom1Feed
from wurdig.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ConstructSlug(formencode.FancyValidator):
    def _to_python(self, value, state):
        if value['slug'] in ['', u'', None]:
            tag_name = value['name'].lower()
            value['slug'] = re.compile(r'[^\w-]+', re.U).sub('-', tag_name).strip('-')
        return value

class UniqueName(formencode.FancyValidator):
    messages = {
        'invalid': 'Tag name must be unique'
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = formencode.validators.UnicodeString(max=30).to_python(value, state)
        # validate that tag only contains letters, numbers, and spaces
        result = re.compile("[^a-zA-Z0-9 ]").search(value)
        if result:
            raise formencode.Invalid("Tag name can only contain letters, numbers, and spaces", value, state)
        
        # Ensure tag name is unique
        tag_q = meta.Session.query(model.Tag).filter_by(name=value)
        if request.urlvars['action'] == 'save':
            # we're editing an existing tag
            tag_q = tag_q.filter(model.Tag.id != int(request.urlvars['id']))
            
        # Check if the tag name exists
        name = tag_q.first()
        if name is not None:
            raise formencode.Invalid(
                self.message('invalid', state),
                value, state)
        
        return value
    
class UniqueSlug(formencode.FancyValidator):
    messages = {
        'invalid': 'Tag slug must be unique'
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = formencode.validators.UnicodeString(max=30).to_python(value, state)
        # validate that slug only contains letters, numbers, and dashes
        result = re.compile("[^\w-]").search(value)
        if result:
            raise formencode.Invalid("Slug can only contain letters, numbers, and dashes", value, state)
        
        # Ensure tag slug is unique
        tag_q = meta.Session.query(model.Tag).filter_by(slug=value)
        if request.urlvars['action'] == 'save':
            # we're editing an existing post.
            tag_q = tag_q.filter(model.Tag.id != int(request.urlvars['id']))
            
        # Check if the slug exists
        slug = tag_q.first()
        if slug is not None:
            raise formencode.Invalid(
                self.message('invalid', state),
                value, state)
        
        return value

class NewTagForm(formencode.Schema):
    pre_validators = [ConstructSlug()]
    allow_extra_fields = True
    filter_extra_fields = True
    name = UniqueName(not_empty=True, max=30, strip=True)
    slug = UniqueSlug(not_empty=True, max=30, strip=True)

class TagController(BaseController):

    def cloud(self):
        return render('/derived/tag/cloud.html')
    
    def category(self, slug=None):   
        if slug is None:
            abort(404)
            
        tag_q = meta.Session.query(model.Tag)
        c.tag = tag_q.filter(model.Tag.slug==slug).count()
        
        if(c.tag in [0, None]):
            abort(404)
            
        return redirect_to(controller='tag', action='archive', slug=slug, _code=301)
    
    def archive(self, slug=None):   
        """
        @todo: purge cache for tag_archive on post add and post delete for post_home
        """
        if slug is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        c.tag = tag_q.filter(model.Tag.slug==slug).first()
        
        if(c.tag is None):
            c.tagname = slug
        else:
            c.tagname = c.tag.name
            
        query = meta.Session.query(model.Post).filter(
            and_(
                 model.Post.tags.any(slug=slug), 
                 model.Post.posted_on != None
            )
        ).all()
            
        c.paginator = paginate.Page(
            query,
            page=int(request.params.get('page', 1)),
            items_per_page = 10,
            controller='tag',
            action='archive',
            slug=slug
        )
                
        return render('/derived/tag/archive.html')

    @beaker_cache(expire=28800, type='memory', cache_key='tag_feed')
    def tag_feed(self, slug=None):
        if slug is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        c.tag = tag_q.filter(model.Tag.slug==slug).first()
        
        if(c.tag is None):
            c.tagname = slug
        else:
            c.tagname = c.tag.name
            
        posts_q = meta.Session.query(model.Post).filter(
            and_(
                 model.Post.tags.any(slug=slug), 
                 model.Post.draft == False 
            )
        ).order_by([model.Post.posted_on.desc()]).limit(10)

        feed = Atom1Feed(
            title=config['blog.title'],
            subtitle=u'Blog posts tagged "%s"' % slug,
            link=u"http://%s%s" % (request.server_name, h.url_for(
                controller='tag',
                action='archive',
                slug=slug
            )),
            description=u"Blog posts tagged %s" % slug,
            language=u"en",
        )
        
        for post in posts_q:
            tags = [tag.name for tag in post.tags]
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
                categories=tuple(tags)
            )
                
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')

    @h.auth.authorize(h.auth.is_valid_user)
    def new(self):
        return render('/derived/tag/new.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewTagForm(), form='new')
    def create(self):
        tag = model.Tag()
        
        for k, v in self.form_result.items():
            setattr(tag, k, v)
        import pprint
        pprint.pprint(tag)
        meta.Session.add(tag)
        meta.Session.commit()
        session['flash'] = 'Tag successfully added.'
        session.save()
        return redirect_to(controller='tag', action='cloud')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def edit(self, id=None):
        if id is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        tag = tag_q.filter_by(id=id).first()
        if tag is None:
            abort(404)
        values = {
            'id':tag.id,
            'name':tag.name,
            'slug':tag.slug
        }
        return htmlfill.render(render('/derived/tag/edit.html'), values)
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewTagForm(), form='edit')
    def save(self, id=None):
        if id is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        tag = tag_q.filter_by(id=id).first()
        if tag is None:
            abort(404)
            
        for k,v in self.form_result.items():
            if getattr(tag, k) != v:
                setattr(tag, k, v)
            
        meta.Session.commit()
        session['flash'] = 'Tag successfully updated.'
        session.save()
        return redirect_to(controller='tag', action='list')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        tags_q = meta.Session.query(model.Tag)
        c.paginator = paginate.Page(
            tags_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 50,
            controller='tag',
            action='list',
        )
        return render('/derived/tag/list.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def delete_confirm(self, id=None):
        if id is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        c.tag = tag_q.filter_by(id=id).first()
        if c.tag is None:
            abort(404)
        return render('/derived/tag/delete_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def delete(self, id=None):
        id = request.params.getone('id')
        tag_q = meta.Session.query(model.Tag)
        tag = tag_q.filter_by(id=id).first()
        if tag is None:
            abort(404)
        # delete post/tag associations
        meta.Session.execute(delete(model.poststags_table, model.poststags_table.c.tag_id==tag.id))
        meta.Session.delete(tag)
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'The tag has been deleted'}"
        else:
            session['flash'] = 'Tag successfully deleted.'
            session.save()
            return redirect_to(controller='page', action='list')
