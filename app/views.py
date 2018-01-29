import os
from app import app, db, lm
from flask import render_template,  g, jsonify, redirect
from flask_login import current_user, login_required
from .models import Restaurant, UserRatings, Media
# #############################################################################
# IMPORTS OF THE ACTUAL BACKEND
# #############################################################################
from user import *
from login import *
from group import *
from errorHandling import *
from restaurant import *
# #############################################################################
# IMPORTS OF THE ACTUAL BACKEND
# #############################################################################

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/api/home/id', methods=['GET'])
def homeApiID():
    if not g.user.is_authenticated:  # user not loggedin
        user = g.user.__dict__
        user['id'] = "-1"
    else:
        user = row2dict(g.user)
    return jsonify(user)

@app.route('/api/', methods=['GET'])
@app.route('/api/home/', methods=['GET'])
def homeApiGet():
    data = {'latestRestaurants': [],
            'latestReviews': []}

    for rest, mediaPath in zip(*Restaurant.latestAdded(5)):
        rest = row2dict(rest)
        rest['mediaPath'] = mediaPath
        data['latestRestaurants'].append(rest)
    for rating, mediaPath, nickname in zip(*UserRatings.latestAdded(5)):
        rating = row2dict(rating)
        rating['mediaPath'] = mediaPath
        rating['nickname'] = nickname
        rating['restaurant'] = row2dict(Restaurant.query.filter_by(id = rating['Restaurant_id']).first())
        data['latestReviews'].append(rating)
    return jsonify(data)
