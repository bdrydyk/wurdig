import datetime
import formencode
import logging
import webhelpers.paginate as paginate
import wurdig.lib.helpers as h

import wurdig.model as model
import wurdig.model.meta as meta

from formencode import htmlfill
from pylons import cache, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.cache import beaker_cache
from pylons.decorators.rest import restrict
from pylons.decorators.secure import authenticate_form
from sqlalchemy.sql import and_, delete
from webhelpers.feedgenerator import Atom1Feed
from wurdig import model
from wurdig.lib.base import BaseController, render

log = logging.getLogger(__name__)
    

class CommentController(BaseController):
    
    @beaker_cache(expire=3600, type='memory', cache_key='comment_feeds')
    def feeds(self):   
        comments_q = meta.Session.query(model.Comment).filter(model.Comment.approved==True)
        comments_q = comments_q.order_by(model.comments_table.c.created_on.desc()).limit(20)
        
        feed = Atom1Feed(
            title=u"Comments for " + h.wurdig_title(),
            subtitle=h.wurdig_subtitle(),
            link=u'http://%s' % request.server_name,
            description=h.wurdig_subtitle(),
            language=u"en",
        )
        
        for comment in comments_q:
            post_q = meta.Session.query(model.Post)
            c.post = comment.post_id and post_q.filter_by(id=int(comment.post_id)).first() or None
            if c.post is not None:
                feed.add_item(
                    title=u"Comment on %s" % c.post.title,
                    link=u'http://%s%s' % (request.server_name, h.url_for(
                        controller='post', 
                        action='view', 
                        year=c.post.posted_on.strftime('%Y'), 
                        month=c.post.posted_on.strftime('%m'), 
                        slug=c.post.slug,
                        anchor=u"comment-" + str(comment.id)
                    )),
                    description=comment.content
                )
                
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
    
    @beaker_cache(expire=14400, type='memory', cache_key='comment_post_comment_feed')
    def post_comment_feed(self, post_id=None):
        if post_id is None:
            abort(404)
        
        post_q = meta.Session.query(model.Post)
        c.post = post_id and post_q.filter(and_(model.Post.id==int(post_id), 
                                                model.Post.draft==False)).first() or None
        if c.post is None:
            abort(404)
        comments_q = meta.Session.query(model.Comment).filter(and_(model.Comment.post_id==c.post.id, 
                                                                   model.Comment.approved==True))
        comments_q = comments_q.order_by(model.comments_table.c.created_on.desc()).limit(10)
        
        feed = Atom1Feed(
            title=h.wurdig_title() + u' - ' + c.post.title,
            subtitle=u'Most Recent Comments',
            link=u'http://%s%s' % (request.server_name, h.url_for(
                    controller='post', 
                    action='view', 
                    year=c.post.posted_on.strftime('%Y'), 
                    month=c.post.posted_on.strftime('%m'), 
                    slug=c.post.slug
                )),
            description=u"Most recent comments for %s" % c.post.title,
            language=u"en",
        )
        
        for comment in comments_q:
            feed.add_item(
                title=c.post.title + u" comment #%s" % comment.id,
                link=u'http://%s%s' % (request.server_name, h.url_for(
                    controller='post', 
                    action='view', 
                    year=c.post.posted_on.strftime('%Y'), 
                    month=c.post.posted_on.strftime('%m'), 
                    slug=c.post.slug,
                    anchor=u'comment-' + str(comment.id)
                )),
                description=comment.content
            )
                
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
    
    def new(self, action, post_id=None):
        if post_id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = post_id and post_q.filter_by(id=int(post_id)).first() or None
        if c.post is None:
            abort(404)
        return render('/derived/comment/new.html')
    
    @restrict('POST')
    @authenticate_form
    @validate(schema=NewCommentForm(), form='new')
    def create(self, action, post_id=None):
        if post_id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = post_id and post_q.filter_by(id=int(post_id)).first() or None
        if c.post is None:
            abort(404)
            
        if not h.auth.authorized(h.auth.is_valid_user) and not h.wurdig_use_akismet():
            if hasattr(self.form_result, 'wurdig_comment_question'):
                del self.form_result['wurdig_comment_question']
            
        comment = model.Comment()
        for k, v in self.form_result.items():
            setattr(comment, k, v)
        comment.post_id = c.post.id

        comment.created_on = datetime.datetime.now()

        comment.content = h.nl2br(comment.content)
        comment.content = h.mytidy(comment.content)
        comment.content = h.comment_filter(comment.content)
        comment.content = h.auto_link(comment.content)
        
        if h.auth.authorized(h.auth.is_valid_user):
            comment.approved = True
            session['flash'] = 'Your comment has been approved.'
        else:
            session['flash'] = 'Your comment is currently being moderated.'
        # @todo: email administrator w/ each new comment
        session.save()
        
        meta.Session.add(comment)
        meta.Session.commit()
                
        return redirect_to(controller='post', 
                           action='view', 
                           year=c.post.posted_on.strftime('%Y'),
                           month=c.post.posted_on.strftime('%m'),
                           slug=c.post.slug
                           )

    @h.auth.authorize(h.auth.is_valid_user)
    def edit(self, id=None):
        if id is None:
            abort(404)
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        if comment is None:
            abort(404)
        values = {
            'name': comment.name,
            'email': comment.email,
            'url': comment.url,
            'content': comment.content,
            'approved' : comment.approved
        }
        return htmlfill.render(render('/derived/comment/edit.html'), values)

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewCommentForm(), form='edit')
    def save(self, id=None):
        if id is None:
            abort(404)
            
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        
        if comment is None:
            abort(404)
            
        if not h.auth.authorized(h.auth.is_valid_user) and not h.wurdig_use_akismet():
            if hasattr(self.form_result, 'wurdig_comment_question'):
                del self.form_result['wurdig_comment_question']
            
        for k,v in self.form_result.items():
            if getattr(comment, k) != v:
                setattr(comment, k, v)
        
        comment.content = h.mytidy(comment.content)
        comment.content = h.auto_link(comment.content)
        
        meta.Session.commit()
        session['flash'] = 'Comment successfully updated.'
        session.save()
        return redirect_to(controller='comment', action='list')

    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        comments_q = meta.Session.query(model.Comment).order_by(
                                                   model.Comment.approved
                                                   ).order_by(model.Comment.created_on.desc())
        comments_q = comments_q.all()
        c.paginator = paginate.Page(
            comments_q,
            page=int(request.params.get('page', 1)),
            items_per_page=20,
            controller='comment',
            action='list'
        )
        return render('/derived/comment/list.html')
     
    """
    @todo: Way too much redundancy below.  This needs to be refactored ... DRY 
    """
    
    @h.auth.authorize(h.auth.is_valid_user)
    def approve_confirm(self, id=None):
        if id is None:
            abort(404)
        comment_q = meta.Session.query(model.Comment)
        c.comment = comment_q.filter_by(id=id).first()
        if c.comment is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = c.comment.post_id and post_q.filter_by(id=int(c.comment.post_id)).first() or None
        if c.post is None:
            abort(404)
        return render('/derived/comment/approve_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def approve(self, id=None):
        id = request.params.getone('id')
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        if comment is None:
            abort(404)
        comment.approved=True
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'The comment has been approved'}"
        else:
            session['flash'] = 'Comment successfully approved.'
            session.save()
            return redirect_to(controller='comment', action='list')
            
    @h.auth.authorize(h.auth.is_valid_user)
    def disapprove_confirm(self, id=None):
        if id is None:
            abort(404)
        comment_q = meta.Session.query(model.Comment)
        c.comment = comment_q.filter_by(id=id).first()
        if c.comment is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = c.comment.post_id and post_q.filter_by(id=int(c.comment.post_id)).first() or None
        if c.post is None:
            abort(404)
        return render('/derived/comment/disapprove_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def disapprove(self, id=None):
        id = request.params.getone('id')
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        if comment is None:
            abort(404)
        comment.approved=False
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'The comment has been approved'}"
        else:
            session['flash'] = 'Comment successfully approved.'
            session.save()
            return redirect_to(controller='comment', action='list')

    @h.auth.authorize(h.auth.is_valid_user)
    def delete_confirm(self, id=None):
        if id is None:
            abort(404)
        comment_q = meta.Session.query(model.Comment)
        c.comment = comment_q.filter_by(id=id).first()
        if c.comment is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = c.comment.post_id and post_q.filter_by(id=int(c.comment.post_id)).first() or None
        if c.post is None:
            abort(404)
        return render('/derived/comment/delete_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def delete(self, id=None):
        id = request.params.getone('id')
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        if comment is None:
            abort(404)
        meta.Session.delete(comment)
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'The comment has been deleted'}"
        else:
            session['flash'] = 'Comment successfully deleted.'
            session.save()
            return redirect_to(controller='comment', action='list')
