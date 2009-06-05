# import helpers as h
# from wurdig.model import *
# from sqlalchemy import desc
# 
# __all__ = ['comment_filter', 'recent_comments']
# 
# def comment_filter(comment):
#     return h.sanitize_html(comment)
# 
# def recent_comments():
#     comments_q = Comment.query.filter_by(approved=True)
#     comments_q.order_by(desc(Comment.created_on)).all()
#     recent_comments = comments_q.limit(4)
#     #recent_comments = comments_q.filter(Comment.post = Post).limit(4)
#     
#     if recent_comments is None:
#         return ''
#     else:
#         comments= []
#         template = """
#         <div id="wurdig-recent-comments" class="wurdig-sidebar-list">
#             <h2>Newest Comments</h2>
#             <ul>
#                 %s
#             </ul>
#         </div>
#         """
# 
#         for comment in recent_comments:
#             i = """
#                 <li class="%s">
#                     <span class="lone">%s shared: </span>
#                     <span>%s</span>
#                     <span>Shared in: %s</span>
#                 </li>
#             """
#             name = comment.name
#             if comment.url is not None:
#                 name = h.link_to(comment.name, comment.url)
#             
#             content = h.truncate(h.strip_tags(comment.content), 80)
#                              
#             link = h.link_to(
#                 comment.post.title,
#                 h.url_for(
#                     controller='post', 
#                     action='view', 
#                     year=comment.post.posted_on.strftime('%Y'), 
#                     month=comment.post.posted_on.strftime('%m'), 
#                     path=comment.post.path,
#                     anchor=u"comment-" + str(comment.id)
#                 )
#             )
#             comments.append(i % (comment.id, name, content, link))
#         return template % '\n'.join(comments)
#     