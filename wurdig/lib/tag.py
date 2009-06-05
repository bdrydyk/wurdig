# import helpers as h
# from pylons import tmpl_context as c
# from wurdig.model import *
# 
# __all__ = ['cloud', 'post_tags']
# 
# def cloud():
#     # grab tag list and x recent comments for display in sidebar
#     tags_q = Session.query(Tag)
#     c.tags = Tag.query.all()
#     if len(c.tags):
#         parts = []
#         parts.append('<div class="hTagCloud"><h4>Tags</h4><ul class="popularity">')
#         for tag in c.tags:
#             parts.append('<li class="%s">' % tag_weight(len(tag.posts)));
#             link_pattern = '<a href="%s" rel="tag" title="%s tagged with %s">%s</a>'
#             url = h.url_for(controller='tag', 
#                              action='archive', 
#                              path=tag.path)
#             parts.append(link_pattern % (url, 
#                                          h.plural(len(tag.posts), 'Post', 'Posts'), 
#                                          tag.name, 
#                                          tag.name)
#             )
#             parts.append('</li>')
#         parts.append('</ul></div>')
# 
#     return '\n'.join(parts)
# 
# def post_tags(tags):
#     if len(tags):
#         parts, _tags = [], []
#         parts.append('<span class="wurdig-entry-tags">')
#         parts.append('<strong>Tagged in</strong> : ')
#         for tag in tags:
#             link_pattern = '<a href="%s" rel="tag">%s</a>'
#             _tags.append(link_pattern % (h.url_for(controller='tag', action='archive', path=tag.path),
#                                          tag.name
#                                          ))
#         tags = ', '.join(_tags)
#         parts.append(tags)
#         parts.append('</span>')
# 
#     return '\n'.join(parts)
# 
# def tag_weight(count):
#     classes = {'level_1' : 'popular', 
#                'level_2' : 'v-popular',
#                'level_3' : 'vv-popular',
#                'level_4' : 'vvv-popular',
#                'level_5' : 'vvvv-popular'}
#     if count in range(1,6):
#         return classes['level_1']
#     elif count in range(7,15):
#         return classes['level_2']
#     elif count in range(16,22):
#         return classes['level_3']
#     elif count in range(23,30):
#         return classes['level_4']
#     elif count > 31:
#         return classes['level_5']
#     else:
#         return ''