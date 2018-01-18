import os
import uuid
from app import app, db, lm
from config import USERPATH, basedir
from flask import render_template, session, request, g, jsonify
from flask_login import login_user, logout_user, login_required
from .models import Media, User
from .forms import SignUpForm, LoginForm
from werkzeug.utils import secure_filename

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

# ##############################################################################
# SIGNUP
# ##############################################################################
@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/api/signup', methods=['GET'])
def signUpApiGet():
    if g.user is not None and g.user.is_authenticated:
        return jsonify({'id': g.user.id}), 201
    user = {'id': '-1',
            'errors': []}
    return jsonify(user), 201


@app.route('/api/signup', methods=['POST'])
def signUpApiPost():
    form = SignUpForm(request.get_json())
    if form.validate():
        avatar = Media(mediaPath = USERPATH + '_defautlUserAvatarSmileyFace.png')
        db.session.add(avatar)
        db.session.commit()

        nickname = form.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        user = User(email = form.email,
                    password = form.password,
                    nickname = nickname,
                    Media_id = avatar.id)
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=form.rememberMe)
        print(user.id, "@@@@@")
        return jsonify({'id': user.id})
    return jsonify({'id': -1, 'errors': form.errors}), 201


# ##############################################################################
# LOGIN
# ##############################################################################
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def loginApiPost():
    print("111")
    form = LoginForm(request.get_json())
    if form.validate():
        user = User.query.filter_by(email = form.email).first()
        login_user(user, remember=form.rememberMe)
        return jsonify({'id': user.id}), 201
    print("@@@")
    return jsonify({'id': -1, 'errors': form.errors}), 201

@app.route('/api/login', methods=['GET'])
def loginApiGet():
    if g.user is not None and g.user.is_authenticated:
        # user = row2dict(g.user)
        return jsonify({'id': g.user.id}), 201
    user = {'id': '-1',
            'errors': []}
    return jsonify(user), 201


# ##############################################################################
# LOGOUT
# ##############################################################################
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('home'))
