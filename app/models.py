from hashlib import md5
from app import db, app
from sqlalchemy import and_
import re
import numpy as np

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}


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
        for group in self.ratedRestaurantGroups(restaurantID):
            print(group.id)
            restaurant.assignNewGroupRating(group)

    def ratedRestaurantGroups(self, restaurantID):
        ratedGroups = db.session.query(
                        Group).join(
                            UsersInGroups).filter(
                                UsersInGroups.User_id == self.id).join(
                                RestaurantsInGroups).filter(
                                    RestaurantsInGroups.Restaurants_id == restaurantID).all()
        print(ratedGroups)
        # return np.array(ratedGroups).ravel().astype(int)
        return ratedGroups



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

    def suggestedRestaurant(self):
        restaurant = RestaurantsInGroups.query.filter(
                        and_(RestaurantsInGroups.Group_id == self.id,
                             RestaurantsInGroups.dailySuggestion == 1)).first()
        if restaurant is not None:
            return Restaurant.query.filter_by(id = restaurant.Restaurants_id).first()




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

    def addReview(self, userID, review):
        userRest = UserRatings.query.filter(
                    and_(UserRatings.User_id.like(userID),
                        UserRatings.Restaurant_id.like(self.id))).first()
        userRest.comment = review
        db.session.add(userRest)
        db.session.commit()

    def getReviews(self):
        reviews = UserRatings.query.\
                    filter(and_(UserRatings.Restaurant_id.like(self.id),
                                UserRatings.comment.isnot(None))).\
                                    order_by(UserRatings.User_id).all()
        users = db.session.query(User).\
                    join(UserRatings).\
                        filter(and_(UserRatings.Restaurant_id.like(self.id),
                                    UserRatings.comment.isnot(None))).\
                                        order_by(User.id).all()
        reviewsList = []
        for user, review in zip(users, reviews):
            print(review.comment)
            mediaPath = Media.query.filter_by(id = user.Media_id).first().mediaPath
            reviewsList.append({'nickname': user.nickname,
                                'mediaPath': mediaPath,
                                'rating': review.rating,
                                'review': review.comment,
                                'userID': user.id})
        return reviewsList

    def generatedTrafic(self, groupID):
        restInGroup = RestaurantsInGroups.query.filter(and_(
                        RestaurantsInGroups.Group_id == groupID,
                        RestaurantsInGroups.Restaurants_id == self.id)).first()
        restInGroup.dailyTraffic += 1
        db.session.add(restInGroup)
        db.session.commit()

    def assignNewGroupRating(self, group):
        GroupRestaurantPair = RestaurantsInGroups.query.filter(
                                and_(RestaurantsInGroups.Restaurants_id.like(self.id),
                                     RestaurantsInGroups.Group_id.like(group.id))).first()
        GroupRestaurantPair.rating = self.calculateGroupRating(group.id)
        db.session.add(GroupRestaurantPair)
        db.session.commit()

class RestaurantsInGroups(db.Model):
    __table__ = db.Model.metadata.tables['RestaurantsInGroups']



class UserRatings(db.Model):
    __table__ = db.Model.metadata.tables['UserRatings']



class Media(db.Model):
    __table__ = db.Model.metadata.tables['Media']

class LoginAttempts(db.Model):
    __table__ = db.Model.metadata.tables['LoginAttempts']

class ResetPassword(db.Model):
    __table__ = db.Model.metadata.tables['ResetPassword']

class PendingUsers(db.Model):
    __table__ = db.Model.metadata.tables['PendingUsers']

class PendingUsersInGroups(db.Model):
    __table__ = db.Model.metadata.tables['PendingUsersInGroups']

class PendingRestaurantsInGroups(db.Model):
    __table__ = db.Model.metadata.tables['PendingRestaurantsInGroups']
