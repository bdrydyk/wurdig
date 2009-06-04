"""Pylons environment configuration"""
import os

from mako.lookup import TemplateLookup
from pylons import config
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config

import wurdig.lib.app_globals as app_globals
import wurdig.lib.helpers
from wurdig.config.routing import make_map
from wurdig.model import init_model
import wurdig.model as model
from sqlalchemy import engine_from_config
import elixir


def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='wurdig', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.h'] = wurdig.lib.helpers
    config['pylons.strict_c'] = True

    # Create the Mako TemplateLookup, with the default auto-escaping
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=paths['templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', default_filters=['escape'],
        imports=['from webhelpers.html import escape'])

    # Setup Elixir
    # note: in this example, I'm leaving connect_args empty, fill in what is right
    # for your app.
    config['pylons.app_globals'].sa_engine = \
        engine_from_config(config, 'sqlalchemy.',
                           connect_args={}, pool_recycle=90)
    elixir.bind = config['pylons.app_globals'].sa_engine
    model.metadata.bind = config['pylons.app_globals'].sa_engine
    elixir.setup_all()

    

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
    
