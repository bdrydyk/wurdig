from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1239585166.5482249
_template_filename='/home/leveille/development/python/pylons/Wurdig/wurdig/templates/base/home.html'
_template_uri='/base/home.html'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['twitter_updates', 'tags', 'title', 'recent_comments', 'development_stream', 'categories', 'archives']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 2
    ns = runtime.Namespace('wurdig', context._clean_inheritance_tokens(), templateuri='../elements/wurdig.html', callables=None, calling_uri=_template_uri, module=None)
    context.namespaces[(__name__, 'wurdig')] = ns

def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, 'wurdig')._populate(_import_ns, ['*'])
        self = _import_ns.get('self', context.get('self', UNDEFINED))
        wurdig = _mako_get_namespace(context, 'wurdig')
        next = _import_ns.get('next', context.get('next', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        # SOURCE LINE 4
        __M_writer(escape(wurdig.doctype()))
        __M_writer(u'\n<html>\n    <head>\n        ')
        # SOURCE LINE 7
        __M_writer(escape(wurdig.meta()))
        __M_writer(u'\n        <title>')
        # SOURCE LINE 8
        __M_writer(escape(self.title()))
        __M_writer(u'</title>\n        ')
        # SOURCE LINE 9
        __M_writer(escape(wurdig.css()))
        __M_writer(u'\n    </head>\n    \n    <body id="home">\n        \n        <div class="container_16">\n            ')
        # SOURCE LINE 15
        __M_writer(escape(wurdig.primary_nav()))
        __M_writer(u'\n        </div>\n        \n        ')
        # SOURCE LINE 18
        __M_writer(escape(wurdig.header()))
        __M_writer(u'\n        \n        <div id="content">\n            <div class="container_16">\n                \n                <div id="primary-content" class="grid_8">\n                    ')
        # SOURCE LINE 24
        __M_writer(escape(wurdig.flash()))
        __M_writer(u'\n                    ')
        # SOURCE LINE 25
        __M_writer(escape(next.body()))
        __M_writer(u'                    \n                </div>\n                \n                <div id="sidebar" class="grid_8">\n                    <div id="twitter-updates">\n                        ')
        # SOURCE LINE 30
        __M_writer(escape(self.twitter_updates()))
        __M_writer(u'\n                    </div>\n                    <div id="categories" class="grid_4 alpha">\n                        ')
        # SOURCE LINE 33
        __M_writer(escape(self.categories()))
        __M_writer(u'\n                    </div>\n                    <div id="archives" class="grid_4 omega">\n                        ')
        # SOURCE LINE 36
        __M_writer(escape(self.archives()))
        __M_writer(u'\n                    </div>\n                    <div id="tags" class="grid_4 alpha">\n                        ')
        # SOURCE LINE 39
        __M_writer(escape(self.tags()))
        __M_writer(u'\n                    </div>\n                    <div id="recent-comments" class="grid_4 omega">\n                        ')
        # SOURCE LINE 42
        __M_writer(escape(self.recent_comments()))
        __M_writer(u'\n                    </div> \n                    <div id="development-stream">\n                        ')
        # SOURCE LINE 45
        __M_writer(escape(self.development_stream()))
        __M_writer(u'\n                    </div>\n                </div>\n            </div>\n        </div>\n        ')
        # SOURCE LINE 50
        __M_writer(escape(wurdig.secondary_content()))
        __M_writer(u'\n        ')
        # SOURCE LINE 51
        __M_writer(escape(wurdig.footer()))
        __M_writer(u'\n        ')
        # SOURCE LINE 52
        __M_writer(escape(wurdig.js()))
        __M_writer(u'      \n    </body>\n</html>\n\n')
        # SOURCE LINE 56
        __M_writer(u'\n\n')
        # SOURCE LINE 66
        __M_writer(u'\n\n')
        # SOURCE LINE 76
        __M_writer(u'\n\n')
        # SOURCE LINE 86
        __M_writer(u'\n\n')
        # SOURCE LINE 96
        __M_writer(u'\n\n')
        # SOURCE LINE 106
        __M_writer(u'\n\n')
        # SOURCE LINE 116
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_twitter_updates(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, 'wurdig')._populate(_import_ns, ['*'])
        __M_writer = context.writer()
        # SOURCE LINE 58
        __M_writer(u'\n    <h4>Twitter Updates</h4>\n    <ul>\n        <li>Update</li>\n        <li>Update</li>\n        <li>Update</li>\n        <li>Update</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_tags(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, 'wurdig')._populate(_import_ns, ['*'])
        __M_writer = context.writer()
        # SOURCE LINE 88
        __M_writer(u'\n    <h4>Tags</h4>\n    <ul>\n        <li>Tag</li>\n        <li>Tag</li>\n        <li>Tag</li>\n        <li>Tag</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, 'wurdig')._populate(_import_ns, ['*'])
        __M_writer = context.writer()
        # SOURCE LINE 56
        __M_writer(u"Jason Leveille's Blog")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_recent_comments(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, 'wurdig')._populate(_import_ns, ['*'])
        __M_writer = context.writer()
        # SOURCE LINE 98
        __M_writer(u'\n    <h4>Recent Comments</h4>\n    <ul>\n        <li>Comment</li>\n        <li>Comment</li>\n        <li>Comment</li>\n        <li>Comment</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_development_stream(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, 'wurdig')._populate(_import_ns, ['*'])
        __M_writer = context.writer()
        # SOURCE LINE 108
        __M_writer(u'\n    <h4>Development Stream</h4>\n    <ul>\n        <li>Link</li>\n        <li>Link</li>\n        <li>Link</li>\n        <li>Link</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_categories(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, 'wurdig')._populate(_import_ns, ['*'])
        __M_writer = context.writer()
        # SOURCE LINE 68
        __M_writer(u'\n    <h4>Categories</h4>\n    <ul>\n        <li>Category</li>\n        <li>Category</li>\n        <li>Category</li>\n        <li>Category</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_archives(context):
    context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, 'wurdig')._populate(_import_ns, ['*'])
        __M_writer = context.writer()
        # SOURCE LINE 78
        __M_writer(u'\n    <h4>Archives</h4>\n    <ul>\n        <li>Archive</li>\n        <li>Archive</li>\n        <li>Archive</li>\n        <li>Archive</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


