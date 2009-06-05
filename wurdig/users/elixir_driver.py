from sqlalchemy import *
from authkit.users import *
from elixir import *
from authkit.users import sqlalchemy_driver

class UsersFromDatabase(sqlalchemy_driver.UsersFromDatabase):
    """
    Database Version
    """
    def _init_(self, model, encrypt=None):
        sqlalchemy_driver.UsersFromDatabase._init_(self, model, encrypt)

    def update_model(self, model):
        class User(Entity):
            has_field("uid", Integer, primary_key=True)
            has_field("username", String(255), unique=True, nullable=False)
            has_field("password", String(255), nullable=False)
            belongs_to('group', of_kind='Group', colname='group_uid')
            using_options(tablename='users')

            def _repr_(self):
                return "User(%(username)s)" % self._dict_

        class Group(Entity):
            has_field('uid', Integer, primary_key=True)
            has_field("name", String(255), unique=True, nullable=False)
            using_options(tablename='groups')

            def _repr_(self):
                return "Group(%(name)s)" % self._dict_

        class Role(Entity):
            has_field("uid", Integer, primary_key=True)
            has_field("name", String(255), unique=True, nullable=False)
            using_options(tablename='roles')

        class UserRole(Entity):
            belongs_to('user', of_kind='User', colname="user_uid")
            belongs_to('role', of_kind='Role', colname="role_uid")
            using_options(tablename='users_roles')

        model.User = User
        model.Group = Group
        model.Role = Role
        return model