import os
import uuid
from app import app, db, lm
from config import USERPATH, basedir
from flask import render_template, session, request, g, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required
from .models import Media, User, LoginAttempts
from .forms import SignUpForm, LoginForm, ResetPasswordForm
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer

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


# ##############################################################################
# RESET
# ##############################################################################
@app.route('/reset/<token>')
def reset(token):
    return render_template('passwordReset.html')

@app.route('/api/reset/<token>', methods=["GET"])
def resetGet(token):
    if g.user is not None and g.user.is_authenticated:
        return jsonify({'logged': True,
                        'errors': ['You are already logged in.']})
    try:
        passwordResetSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = passwordResetSerializer.loads(token, salt='password-reset-salt', max_age=7200)
    except:
        return jsonify({'expired': True})

    print(email, "!!!")

    user = User.query.filter_by(email = email).first()
    if not user.isLocked():
        return jsonify({'expired': True})
    return jsonify({'email': email})


@app.route('/api/reset/<token>', methods=["POST"])
def resetPost(token):

    form = ResetPasswordForm(request.get_json())
    if form.validate():
        user = User.query.filter_by(email = form.email).first()
        user.password = form.password
        db.session.add(user)
        db.session.commit()
        user.unlock()
        return jsonify({'unlocked': True})

    return jsonify({'errors': form.errors})
