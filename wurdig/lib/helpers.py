"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from routes import url_for
from webhelpers.html import literal
from webhelpers.html.secure_form import secure_form
from webhelpers.html.tags import *
from webhelpers.html.tools import auto_link, mail_to
from webhelpers.text import truncate, chop_at, plural
from webob.exc import strip_tags

from wurdig.lib import auth
from wurdig.lib.comment import *
from wurdig.lib.conf_helper import *
from wurdig.lib.feed_display import *
from wurdig.lib.html import *
from wurdig.lib.mdown import *
from wurdig.lib.tag import cloud, post_tags
from wurdig.lib.tidy_helper import *
from wurdig.lib.utils_helper import *
from webhelpers.html.tags import stylesheet_link
from webhelpers.html.tags import javascript_link