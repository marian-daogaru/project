# -*- coding: utf-8 -*-
import os
import uuid
import time
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

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
def pr(x, y):
    print("task cron test {} {} {}".format(1, 2, time.time()))
    time.sleep(2)
JOBS = [{
    'id' : 'job1', #str(uuid.uuid4().hex),
    'func': 'app.emailManager:pr',
    # 'args': (1, 2),
    'trigger': 'cron',
    'second': '*/5',
    # 'minute': '*/5',
    # 'hour': '*',
    'replace_existing': True,
    'max_instances': 1,
}]
SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
        }
SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
SCHEDULER_API_ENABLED = True
