from hashlib import md5
from app import db, app
from sqlalchemy import and_
import re
import numpy as np


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
            print("@@@", dir(UsersInGroups.query.filter(and_(UsersInGroups.User_id.like(user.id),
                                                    UsersInGroups.Group_id.like(group.id)))))#.delete()
            UsersInGroups.query.filter(and_(UsersInGroups.User_id.like(user.id),
                                            UsersInGroups.Group_id.like(group.id))).delete(synchronize_session='fetch')
            db.session.commit()

    def joinedGroups(self):
        return Group.query.join(
            UsersInGroups, (UsersInGroups.Group_id == Group.id)).filter(
            UsersInGroups.User_id == self.id).order_by(Group.name.desc())

    def isAdmin(self, groupID):
        return UsersInGroups.query.filter(and_(UsersInGroups.User_id.like(self.id),
                                                UsersInGroups.Group_id.like(groupID))).first().admin

    def rateRestaurant(self, restaurantID, rating):
        userRate = UserRatings.query.filter(
                        and_(UserRatings.User_id.like(self.id),
                             UserRatings.Restaurant_id.like(restaurantID))).first()
        if userRate is None:
            userRate = UserRatings(User_id = self.id,
                                   Restaurant_id = restaurantID)
        userRate.rating = rating
        db.session.add(userRate)
        db.session.commit()
        restaurant = Restaurant.query.filter_by(id = restaurantID).first()
        for groupID in self.ratedRestaurantGroups(restaurantID):
            print(groupID)
            rating = restaurant.calculateGroupRating(groupID)
            GroupRestaurantPair = RestaurantsInGroups.query.filter(
                                    and_(RestaurantsInGroups.Restaurants_id.like(restaurantID),
                                         RestaurantsInGroups.Group_id.like(groupID))).first()
            print(GroupRestaurantPair, restaurantID, type(groupID), rating)
            GroupRestaurantPair.rating = rating
            db.session.add(GroupRestaurantPair)
            db.session.commit()

    def ratedRestaurantGroups(self, restaurantID):
        ratedGroups = db.session.query(
                        Group.id).join(
                            UsersInGroups).filter(
                                UsersInGroups.User_id == self.id).join(
                                RestaurantsInGroups).filter(
                                    RestaurantsInGroups.Restaurants_id == restaurantID).all()

        return np.array(ratedGroups).ravel().astype(int)





class UsersInGroups(db.Model):
    __table__ = db.Model.metadata.tables['UsersInGroups']



class Group(db.Model):
    __table__ = db.Model.metadata.tables['Group']

    # def __repr__(self):
    #     return '<Group {}'.format(self.aboutGroup)
    def users(self):
        return UsersInGroups.query.filter_by(Group_id = self.id).all()

    def restaurants(self):
        query = db.session.query(RestaurantsInGroups.Restaurants_id).\
                    filter(RestaurantsInGroups.Group_id == self.id).subquery()

        return db.session.query(Restaurant).join(query)

    def lastAdmin(self):
        adminCount = UsersInGroups.query.filter(
                        and_(UsersInGroups.Group_id.like(self.id),
                             UsersInGroups.admin.like(1))).count()
        return adminCount <= 1

    def makeAdmin(self, userID):
        userInGroup = UsersInGroups.query.filter(
                        and_(UsersInGroups.Group_id.like(self.id),
                             UsersInGroups.User_id.like(userID))).first()
        userInGroup.admin = 1
        db.session.commit()






class Restaurant(db.Model):
    __table__ = db.Model.metadata.tables['Restaurant']

    @staticmethod
    def searchName(name):
        # dir()
        restaurantNames = np.array(db.session.query(Restaurant.name).distinct().all()).ravel()
        matched = [restaurant for restaurant in restaurantNames if name.lower() in restaurant.lower()]
        print(restaurantNames, matched)
        if len(matched) > 0:
            restaurants = [Restaurant.query.filter_by(name = match).first() for match in matched]
            return restaurants
        else:
            return False

    @staticmethod
    def addToDatabase(name, url, mediaPath):
        media = Media(mediaPath = mediaPath)
        db.session.add(media)
        db.session.commit()

        restaurant = Restaurant(name = name,
                                website = url,
                                Media_id = media.id)
        db.session.add(restaurant)
        db.session.commit()
        return restaurant


    def inGroup(self, group):
        return RestaurantsInGroups.query.filter_by(
                    Restaurants_id = self.id).filter_by(
                        Group_id = group.id).count() > 0

    def addToGroup(self, group):
        if not self.inGroup(group):
            new = RestaurantsInGroups(Group_id = group.id,
                                      Restaurants_id = self.id,
                                      rating = -1)
            db.session.add(new)
            db.session.commit()

    def mediaPath(self):
        return Media.query.filter_by(id = self.Media_id).first().mediaPath

    def currentOverallRating(self):
        ratings = db.session.query(UserRatings.rating).filter(
                    UserRatings.Restaurant_id == self.id).all()
        ratings = np.array(ratings).ravel().astype(int)
        if ratings.shape[0] == 0 or (ratings != 0).sum() == 0:
            return -1
        else:
            return np.average(ratings[ratings != 0])

    def currentUserRating(self, user):
        if self.isCurrentUserRating(user):
            return UserRatings.query.filter_by(
                        User_id = user.id).filter_by(
                            Restaurant_id = self.id).first().rating
        else:
            return 0

    def isCurrentUserRating(self, user):
        return UserRatings.query.filter_by(User_id = user.id).filter_by(
                                    Restaurant_id = self.id).count() > 0

    def groupRating(self, groupID):
        #to get the group rating from the stored version
        return RestaurantsInGroups.query.filter(
                and_(RestaurantsInGroups.Restaurants_id.like(self.id),
                     RestaurantsInGroups.Group_id.like(groupID))).first().rating


    def calculateGroupRating(self, groupID):
        ratings = db.session.query(UserRatings.rating).join(
                    User).join(
                        UsersInGroups).filter(
                            UsersInGroups.Group_id == groupID).filter(
                                UserRatings.Restaurant_id == self.id).all()
        ratings = np.array(ratings).ravel().astype(int)
        # print(ratings, 'hello ###', np.average(ratings))
        if 0 in ratings:
            return 0
        elif ratings.shape[0] == 0:
            return -1
        else:
            return np.average(ratings)




class RestaurantsInGroups(db.Model):
    __table__ = db.Model.metadata.tables['RestaurantsInGroups']



class UserRatings(db.Model):
    __table__ = db.Model.metadata.tables['UserRatings']



class Media(db.Model):
    __table__ = db.Model.metadata.tables['Media']
