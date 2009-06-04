"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm, schema, types, func
from sqlalchemy.orm import column_property
from sqlalchemy.sql import and_, select

import datetime
from sqlalchemy import orm
from sqlalchemy.orm import scoped_session, sessionmaker
import elixir


from sqlalchemy import engine_from_config
# replace the elixir session with our own
Session = scoped_session(sessionmaker(autoflush=True, transactional=True))
elixir.session = Session
elixir.options_defaults.update({
    'shortnames': True
})

# use the elixir metadata
metadata = elixir.metadata

# this will be called in config/environment.py
def init_model(engine):
    metadata.bind = engine

# import your entities, and set them up
from entities import *
elixir.setup_all()
