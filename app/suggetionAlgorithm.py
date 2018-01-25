import numpy as np
from sqlalchemy import and_

# ##############################################################################
# CUSTOM IMPORTS
# ##############################################################################
from app import app, db
from models import Group, Restaurant, Media, User, UsersInGroups, RestaurantsInGroups


class SuggestionGenerator(object):
    def __init__(self):
        self.resetDailySuggestion()
        self.generateSuggestion()
        print("!@!@!@")

    def getSuggestion(self, group):
        restaurant = RestaurantsInGroups.query.\
                        filter(and_(
                            RestaurantsInGroups.dailySuggestion == 1,
                            RestaurantsInGroups.Group_id == group.id)).first()

        if restaurant is not None:
            return Restaurant.query.filter_by(id = restaurant.Restaurants_id).first()


    def generateSuggestionGroup(self, group):
        data = self.filterData(group)

        if len(data) > 0:
            data[:, 2] += 1  # so we can exclude the cases where we have 0 traffic for that page
            maximumValues = np.max(data, axis=0)[1:]
            data[:, 1][data[:, 1] == -1] += 4
            size = data.shape[0]
            values = 2 * np.random.uniform(0.9, 1.1, size) * data[:, 1] / maximumValues[0] + \
                     np.random.uniform(0.9, 1.1, size) * data[:, 2] / maximumValues[1] + \
                     np.random.uniform(0.9, 1.1, size) * data[:, 3] / maximumValues[2]

            restaurant = RestaurantsInGroups.query.\
                            filter(and_(
                                RestaurantsInGroups.Restaurants_id == data[values.argmax(), 0],
                                RestaurantsInGroups.Group_id == group.id)).first()
            restaurant.dailySuggestion = 1
            restaurant.lastSuggested = 0
            db.session.add(restaurant)
            db.session.commit()

    def generateSuggestion(self):
        groups = db.session.query(Group).join(RestaurantsInGroups).distinct().all()
        for group in groups:
            self.generateSuggestionGroup(group)

    def getRestaurants(self, group):
        return RestaurantsInGroups.query.filter_by(Group_id = group.id).all()

    def extractArrays(self, group):
        data = db.session.query(RestaurantsInGroups.Restaurants_id,
                               RestaurantsInGroups.rating,
                               RestaurantsInGroups.dailyTraffic,
                               RestaurantsInGroups.lastSuggested).\
                filter_by(Group_id = group.id).all()

        data = np.array(data)
        return data

    def filterData(self, group):
        data = self.extractArrays(group)
        if data.shape[0] == 0:
            return []
        data = data[data[:, 1] != 0]
        return data

    def increaseLastSuggested(self):
        db.session.query(RestaurantsInGroups).update(
            {RestaurantsInGroups.lastSuggested: RestaurantsInGroups.lastSuggested + 1},
               synchronize_session=False)
        db.session.commit()

    def resetDailyTraffic(self):
        RestaurantsInGroups.query.update(
            {RestaurantsInGroups.dailyTraffic: 0},
            synchronize_session=False)
        db.session.commit()

    def resetDailySuggestion(self):
        RestaurantsInGroups.query.update(
            {RestaurantsInGroups.dailySuggestion: 0},
            synchronize_session=False)
        db.session.commit()

    def resetTraffic(self):
        self.resetDailyTraffic()
        self.increaseLastSuggested()
