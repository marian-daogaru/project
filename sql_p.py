import MySQLdb
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/projectDB'
db = SQLAlchemy(app)

print(dir(db))
