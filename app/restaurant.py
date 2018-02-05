import os
import uuid
import numpy as np
from app import app, db, lm
from config import USERPATH, basedir
from flask import render_template, session, request, g, jsonify, flash, redirect
from flask_login import login_required
from .models import Media, User, Group, Restaurant, RestaurantsInGroups, RestaurantDetails
from .forms import RestaurantAddForm, ReviewForm
from werkzeug.utils import secure_filename

from restaurantExtraction import extractRestaurant

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}


# ##############################################################################
# ADD RESTAURANT PART
# ##############################################################################

@app.route('/group/<id>/addRestaurant')
@login_required
def addRestaurant(id):
    return render_template('addRestaurant.html')


@app.route('/api/group/<id>/addRestaurant', methods=['GET'])
@login_required
def addRestaurantGet(id):
    group = Group.query.filter_by(id = id).first()
    if group is not None and g.user.isInGroup(g.user, group):
        print(request.get_json(), 222)
        return jsonify(row2dict(group))

    return jsonify({'accessDenied': True})

# ##############################################################################
# SEARCH
# ##############################################################################
@app.route('/api/group/<id>/addRestaurant/<string:name>', methods=['GET'])
@login_required
def addRestaurantGetRestaurantSearch(id, name):
    group = Group.query.filter_by(id = id).first()
    if g.user.isInGroup(g.user, group):
        restaurants = Restaurant.advancedSearchName(name)
        restaurantsList = []
        if restaurants is not None:
            for restaurant in restaurants:
                if not restaurant.inGroup(group):
                    restaurant = row2dict(restaurant)
                    restaurant['mediaPath'] = Media.query.filter_by(
                                                id = restaurant['Media_id']).first().mediaPath
                    restaurantsList.append(restaurant)
            print(restaurantsList)
        return jsonify(restaurantsList)
    return jsonify({'accessDenied': True})



# ##############################################################################
# GENERAL SEARCH
# ##############################################################################
@app.route('/restaurant/search/<name>')
@login_required
def searchRestaurant(name):
    return render_template('searchRestaurant.html')

@app.route('/api/restaurant/search/<name>', methods=['GET'])
@login_required
def searchRestaurantGet(name):
    if len(name) > 0:
        restaurants = Restaurant.advancedSearchName(name)
        restaurantsList = []
        if restaurants is not None:
            for restaurant in restaurants:
                rating = restaurant.currentOverallRating()
                restaurant = row2dict(restaurant)
                restaurant['mediaPath'] = Media.query.filter_by(
                                            id = restaurant['Media_id']).first().mediaPath
                restaurant['rating'] = rating
                restaurantsList.append(restaurant)
        print(restaurantsList)
        return jsonify(restaurantsList)

    return jsonify({'accessDenied': True})


# ##############################################################################
# ADD RESTAURANT
# ##############################################################################
@app.route('/api/group/<id>/addRestaurant', methods=['POST'])
@login_required
def addRestaurantPost(id):
    response = request.get_json()
    print(response)
    form = RestaurantAddForm(response)

    if form.validate():
        restaurantBasic, details = extractRestaurant(form.url)
        print(restaurant)
        restaurant = Restaurant.query.filter_by(website = form.url).first()
        print(restaurant)
        if restaurant is None:
            restaurant = Restaurant.addToDatabase(restaurantBasic[0],
                                                  form.url,
                                                  restaurantBasic[1],
                                                  details)
        group = Group.query.filter_by(id = id).first()
        if g.user.isAdmin(group.id):
            print("Group added bacause admin!")
            restaurant.addToGroup(group)
        else:
            print("Group !added bacause !admin!")
            restaurant.addToPending(group)
            group.emailAdminsUpdate()
        return jsonify({'confirmations': ['Restaurant added succesfully!']})
    return jsonify({'errors': form.errors})


@app.route('/api/group/<id>/addRestaurant/<ids>', methods=['PUT'])
@login_required
def addRestaurantPut(id, ids):
    group = Group.query.filter_by(id = id).first()
    ids = ids.split(',')
    print(ids, type(ids))
    if len(ids) != 0:
        for restaurantID in ids:
            restaurant = Restaurant.query.filter_by(id = restaurantID).first()
            if restaurant is None:
                return jsonify({'errors': ['No such restaurant. This is a bug.']})
            if g.user.isAdmin(group.id):
                print("Group added bacause admin!")
                restaurant.addToGroup(group)
            else:
                print("Group !added bacause !admin!")
                restaurant.addToPending(group)
            print(restaurant.calculateGroupRating(group.id), "RATINGS")
        if g.user.isAdmin(group.id):
            group.emailAdminsUpdate()
        return jsonify({'confirmations': ['Restaurants added succesfully!']})
    else:
        return jsonify({'nothing': ['Nothing Happened. BUG!']})



# ##############################################################################
# RESTAURANT PROFILE
# ##############################################################################
@app.route('/restaurant/<id>')
@login_required
def restaurant(id):
    return render_template('restaurant.html')

@app.route('/api/restaurant/<id>', methods=['GET'])
@login_required
def restaurantGet(id):
    restaurant = Restaurant.query.filter_by(id = id).first()
    if restaurant is None:
        return jsonify({'errors': ['No such restaurant. This is a bug.']})
    mediaPath = Media.query.filter_by(id = restaurant.Media_id).first().mediaPath
    rating = restaurant.currentOverallRating()
    restaurant = row2dict(restaurant)
    restaurant['mediaPath'] = mediaPath
    restaurant['rating'] = rating
    details = RestaurantDetails.query.filter_by(Restaurant_id = restaurant['id']).first()
    if details is not None:
        details.tags = str(details.tags.replace(', ', ',').replace(',', ', '))  # some legacy problems
        restaurant['details'] = row2dict(details)
        print((restaurant['details']['tags']).split(', '), 222)
        restaurant['details']['tags'] = restaurant['details']['tags'].split(', ')
    return jsonify(restaurant)


# ##############################################################################
# RESTAURANT PROFILE FOR DATA SCRAPING
# ##############################################################################

@app.route('/group/<groupID>/restaurant/<restID>')
@login_required
def restaurantInGroup(groupID, restID):
    return render_template('restaurant.html')

@app.route('/api/group/<groupID>/restaurant/<restID>', methods=['GET'])
@login_required
def restaurantinGroupGet(groupID, restID):
    restaurant = Restaurant.query.filter_by(id = restID).first()
    group = Group.query.filter_by(id = groupID).first()
    if restaurant is None or group is None:
        return jsonify({'errors': ['No such restaurant. This is a bug.']})
    if not restaurant.inGroup(group):
        return jsonify({'errors': ['Restaurant not in that group.']})
    mediaPath = Media.query.filter_by(id = restaurant.Media_id).first().mediaPath
    rating = restaurant.currentOverallRating()
    restaurant = row2dict(restaurant)
    restaurant['mediaPath'] = mediaPath
    restaurant['rating'] = rating
    restaurant['groupID'] = groupID
    details = RestaurantDetails.query.filter_by(Restaurant_id = restaurant['id']).first()
    if details is not None:
        details.tags = str(details.tags.replace(', ', ',').replace(',', ', '))  # some legacy problems
        restaurant['details'] = row2dict(details)
        print(restaurant['details'])
        restaurant['details']['tags'] = restaurant['details']['tags'].split(', ')
    return jsonify(restaurant)

@app.route('/api/group/<groupID>/restaurant/<restID>', methods=['PUT'])
@login_required
def restaurantinGroupPut(groupID, restID):
    restaurant = Restaurant.query.filter_by(id = restID).first()
    group = Group.query.filter_by(id = groupID).first()
    if restaurant is None or group is None:
        return jsonify({'errors': ['No such restaurant. This is a bug.']})
    if not restaurant.inGroup(group):
        return jsonify({'errors': ['Restaurant not in that group.']})

    restaurant.generatedTrafic(groupID)
    return jsonify({})


# ##############################################################################
# RESTAURANT REVIEW GENERAL
# ##############################################################################
@app.route('/api/restaurant/<id>/reviews', methods=['GET'])
@login_required
def restaurantReviewGeneralGet(id):
    print("HELLO")
    restaurant = Restaurant.query.filter_by(id = id).first()
    if restaurant is None:
        return jsonify({'notFound': True})
    reviews = restaurant.getReviewsGeneral()
    return jsonify(reviews)


@app.route('/api/restaurant/<id>/user/<userID>/<review>', methods=['PUT'])
@login_required
def restaurantReviewGeneralPut(id, userID, review):
    print("HEY @")
    restaurant = Restaurant.query.filter_by(id = id).first()
    if restaurant is not None:
        if int(g.user.id) == int(userID):
            form = ReviewForm(review)
            if form.validate():
                restaurant.addReview(userID, review)
                return jsonify({'added': True})
            return jsonify({'errors': form.errors})
        return jsonify({'accessDenied': True})
    return jsonify({'error': ['Restaurant not found']})


# ##############################################################################
# RESTAURANT REVIEW GROUP
# ##############################################################################
@app.route('/api/group/<groupID>/restaurant/<id>/reviews', methods=['GET'])
@login_required
def restaurantReviewGroupGet(groupID, id):
    print("HELLOOOOOOOOO")
    restaurant = Restaurant.query.filter_by(id = id).first()
    if restaurant is None:
        return jsonify({'notFound': True})
    reviews = restaurant.getCommentsGroup(groupID)

    return jsonify(reviews)


@app.route('/api/group/<groupID>/restaurant/<id>/user/<userID>/<comment>', methods=['PUT'])
@login_required
def restaurantReviewGroupPut(groupID, id, userID, comment):
    print("HEEEYY!")
    restaurant = Restaurant.query.filter_by(id = id).first()
    if restaurant is not None:
        group = Group.query.filter_by(id = groupID).first()
        if group is not None:
            if int(g.user.id) == int(userID) or not restaurant.inGroup(group):
                form = ReviewForm(comment)
                if form.validate():
                    restaurant.addComment(groupID, userID, comment)
                    return jsonify({'added': True})
                return jsonify({'errors': form.errors})
            return jsonify({'accessDenied': True})
        return jsonify({'error': ['Group not found']})
    return jsonify({'error': ['Restaurant not found']})


# ##############################################################################
# PENDING RESTAURANT
# ##############################################################################
@app.route('/group/<id>/edit/pendingRestaurants')
@login_required
def editPendingRestaurants(id):
    return render_template('pendingRestaurants.html')

@app.route('/api/group/<id>/edit/pendingRestaurants', methods=['GET'])
@login_required
def editPendingRestaurantsGet(id):
    group = Group.query.filter_by(id = id).first()
    if g.user.isInGroup(g.user, group) and g.user.isAdmin(group.id):
        pendingRests = group.pendingRestaurants()
        pendingMedia = group.pendingRestaurantsMedia()
        print(pendingRests, pendingMedia)
        restaurants = []
        for restaurant, mediaPath in zip(pendingRests, pendingMedia):
            print(mediaPath)
            restaurant = row2dict(restaurant)
            restaurant['mediaPath'] = mediaPath
            restaurants.append(restaurant)
        print(restaurants)
        return jsonify({'restaurants': restaurants,
                        'groupID': group.id})
    return jsonify({'accessDenied': True})

@app.route('/api/group/<id>/edit/pendingRestaurants/<ids>', methods=['PUT'])
@login_required
def editPendingRestaurantsPut(id, ids):
    group = Group.query.filter_by(id = id).first()
    print(ids, len(ids), "@@@")
    if len(ids) == 0:
        return jsonify({'errors': ['No restaurants!']})
    if g.user.isInGroup(g.user, group) and g.user.isAdmin(group.id):
        ids = np.array(ids.split(',')).astype(int)
        group.addPendingRestaurants(ids)
        return jsonify({'confirmations': ['Restaurants added succesfully.']})
    return jsonify({'accessDenied': True})

@app.route('/api/group/<id>/edit/pendingRestaurants/<ids>', methods=['DELETE'])
@login_required
def editPendingRestaurantsDelete(id, ids):
    group = Group.query.filter_by(id = id).first()
    print(ids, len(ids), "@@@ REMOVE")
    if len(ids) == 0:
        return jsonify({'errors': ['No restaurants!']})
    if g.user.isInGroup(g.user, group) and g.user.isAdmin(group.id):
        ids = np.array(ids.split(',')).astype(int)
        group.removePendingRestaurants(ids)
        return jsonify({'confirmations': ['Restaurants removed succesfully.']})
    return jsonify({'accessDenied': True})
