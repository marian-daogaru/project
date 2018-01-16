import os
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from flask_jsglue import JSGlue
import wtforms_json



app = Flask(__name__)
CORS(app)
jsglue = JSGlue(app)
app.config.from_object('config')
wtforms_json.init()
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = 'Please log in to access this page.'

# db = MySQLdb.connect(host="localhost",
#                      user="root",
#                      passwd="root",
#                      db='projectDB')


db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)




# print(dir(db))

from app import views  # this will be always at the end
