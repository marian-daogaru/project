from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .models import Group




@app.route('/')
@app.route('/home')
def home():
    print(dir(Group.query))
    grps = Group.query.all()
    for grp in grps:
        print('!!!!', grp.aboutGroup)
    return render_template('home.html')
