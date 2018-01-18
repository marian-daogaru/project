import os
from app import app, db, lm
from flask import render_template,  g, jsonify, redirect
from flask_login import current_user, login_required

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


@app.route('/api/', methods=['GET'])
@app.route('/api/home', methods=['GET'])
def homeApi():
    if not g.user.is_authenticated:  # user not loggedin
        user = g.user.__dict__
        user['id'] = "-1"
    else:
        user = row2dict(g.user)
    return jsonify(user)
