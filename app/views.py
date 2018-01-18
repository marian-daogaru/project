import os
from datetime import timedelta
import uuid
import numpy as np
import json
from app import app, db, lm
from config import USERPATH, GROUPPATH, basedir
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .models import Group, Media, User, UsersInGroups
from .forms import SignUpForm, LoginForm, EditForm, GroupCreateForm,  EditGroupForm, PeopleGroupForm
from werkzeug.utils import secure_filename

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

# #############################################################################
# IMPORTS OF THE ACTUAL BACKEND
# #############################################################################
from user import *
from login import *
from group import *
from errorHandling import *
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
