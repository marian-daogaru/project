from hashlib import md5
from app import db, app
import re


class User(db.Model):
    __table__ = db.Model.metadata.tables['User']


    @staticmethod
    def isValidPassword(password):
        return not bool(re.compile(r'[^a-zA-Z0-9_\.]'))

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub(r'^[a-zA-Z0-9_\.]', '', nickname)

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
        # self.id = User.query.filter_by(email = self.email).first().id
        try:
            print(unicode(self.id), '!!!', type(self.id), self.password)
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def get_avatar(self):
        return UserAvatar.query.filter_by(
                 UserAvatar.User_id == self.id).first()   # NMOT SURE DOUGH...

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
    __table__ = db.Model.metadata.tables['Restaurant']


class RestaurantAvatar(db.Model):
    __table__ = db.Model.metadata.tables['RestaurantAvatar']
