import os
import uuid
from app import app, db, lm
from config import USERPATH, basedir
from flask import render_template, session, request, g, jsonify, flash, redirect
from flask_login import login_required
from .models import Media, User, Group, Restaurant
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
        print(name, 222)
        restaurants = Restaurant.searchName(name)
        restaurantsList = []
        if restaurants:
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
        print(name)
        restaurants = Restaurant.searchName(name)
        restaurantsList = []
        if restaurants:
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
        restaurantName, restaurantMediaPath = extractRestaurant(form.url)
        print(restaurantName, restaurantMediaPath)
        restaurant = Restaurant.query.filter_by(website = form.url).first()
        print(restaurant)
        if restaurant is None:
            restaurant = Restaurant.addToDatabase(restaurantName[:30],
                                                  form.url,
                                                  restaurantMediaPath)
        group = Group.query.filter_by(id = id).first()
        restaurant.addToGroup(group)
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
            restaurant.addToGroup(group)
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
# RESTAURANT REVIEW
# ##############################################################################
@app.route('/api/restaurant/<id>/reviews', methods=['GET'])
@login_required
def restaurantReviewGet(id):
    restaurant = Restaurant.query.filter_by(id = id).first()
    if restaurant is None:
        return jsonify({'notFound': True})
    reviews = restaurant.getReviews()
    return jsonify(reviews)



@app.route('/api/restaurant/<id>/user/<userID>/<review>', methods=['PUT'])
@login_required
def restaurantReviewPut(id, userID, review):
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
