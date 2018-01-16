from hashlib import md5
from app import db, app
from sqlalchemy import and_
import re


class User(db.Model):
    __table__ = db.Model.metadata.tables['User']

    @staticmethod
    def isValidPassword(password):
        return not bool(re.compile(r'[^a-zA-Z0-9_\.]'))

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub(r'[^a-zA-Z0-9_\.]', '', nickname)

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

    def get_avatar(self):
        return Media.query.filter_by(
                 id = self.Media_id).first()   # NMOT SURE DOUGH...

    def isInGroup(self, user, group):
        # print("### DIR UsersInGroups", dir(UsersInGroups))
        return UsersInGroups.query.filter_by(User_id = user.id).filter_by(
                                    Group_id = group.id).count() > 0

    def joinGroup(self, user, group):
        if not self.isInGroup(user, group):
            new = UsersInGroups(User_id = user.id,
                                Group_id = group.id)
            db.session.add(new)
            db.session.commit()
            return new

    def leaveGroup(self, user, group):
        if self.isInGroup(user, group):
            print("@@@", UsersInGroups.query.filter(and_(UsersInGroups.User_id.like(user.id),
                                                    UsersInGroups.Group_id.like(group.id))))#.delete()
            # db.session.commit()

    def joinedGroups(self):
        return Group.query.join(
            UsersInGroups, (UsersInGroups.Group_id == Group.id)).filter(
            UsersInGroups.User_id == self.id).order_by(Group.name.desc())

    def isAdmin(self, groupID):
        return UsersInGroups.query.filter(and_(UsersInGroups.User_id.like(self.id),
                                                UsersInGroups.Group_id.like(groupID))).first().admin

    # TODO the rest of the the functions


class UsersInGroups(db.Model):
    __table__ = db.Model.metadata.tables['UsersInGroups']



class Group(db.Model):
    __table__ = db.Model.metadata.tables['Group']

    # def __repr__(self):
    #     return '<Group {}'.format(self.aboutGroup)
    def users(self):
        return UsersInGroups.query.filter_by(Group_id = self.id).all()


class Restaurant(db.Model):
    __table__ = db.Model.metadata.tables['Restaurant']

class Media(db.Model):
    __table__ = db.Model.metadata.tables['Media']
