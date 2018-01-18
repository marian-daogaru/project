import os
import uuid
from app import app, db, lm
from config import USERPATH, basedir
from flask import render_template, session, request, g, jsonify, flash, redirect
from flask_login import login_required
from .models import Media, User, Group, Restaurant
from .forms import RestaurantAddForm
from werkzeug.utils import secure_filename

from restaurantExtraction import extractRestaurant

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}


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
        return jsonify(restaurantsList)

    return jsonify({'accessDenied': True})


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
