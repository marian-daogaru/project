from hashlib import md5
from app import db, app
import re


class User(db.Model):
    __table__ = db.Model.metadata.tables['User']

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    # TODO the rest of the the functions


class UserAvatar(db.Model):
    __table__ = db.Model.metadata.tables['UserAvatar']


class Group(db.Model):
    __table__ = db.Model.metadata.tables['Group']

    # def __repr__(self):
    #     return '<Group {}'.format(self.aboutGroup)


class GroupAvatar(db.Model):
    __table__ = db.Model.metadata.tables['GroupAvatar']


class Restaurant(db.Model):
    __table__ = db.Model.metadata.tables['Restaurants']


class RestaurantAvatar(db.Model):
    __table__ = db.Model.metadata.tables['RestaurantAvatar']
