# -*- coding: utf-8 -*-
import os
import uuid
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
# SECRET_KEY = str(uuid.uuid4())
SECRET_KEY = 'hello'
# CACHE FOR STATIC FILES - used so the js will actually be loaded
SEND_FILE_MAX_AGE_DEFAULT = 0

# SQL ALCHEMY MySQL path
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/projectDB'

# PATHS
GROUPPATH = '../static/data/media/avatars/groups/'
USERPATH = '../static/data/media/avatars/users/'
RESTAURANTPATH = '../static/data/media/avatars/restaurants/'



# administrator list
ADMINS = ['marian@phyramid.com']
