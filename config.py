# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# CACHE FOR STATIC FILES - used so the js will actually be loaded
SEND_FILE_MAX_AGE_DEFAULT = 0

# SQL ALCHEMY MySQL path
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/projectDB'

# PATHS
GROUPPATH = '../static/data/media/avatars/groups/'
USERPATH = '../static/data/media/avatars/users/'
RESTAURANTPATH = '../static/data/media/avatars/restaurants/'

# mail server settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'mdaogaru.test'
MAIL_PASSWORD = 'MarianDaogar9'

# administrator list
ADMINS = ['marian@phyramid.com']
