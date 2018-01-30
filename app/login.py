import os
import uuid
import requests
from app import app, db, lm, recaptcha
from config import USERPATH, basedir
from privateData import RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY
from flask import render_template, session, request, g, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required
from .models import Media, User, LoginAttempts, PendingUsers
from .forms import SignUpForm, LoginForm, ResetPasswordForm, ResetRequestForm
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
        nickname = form.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        user = PendingUsers(email = form.email,
                    password = form.password,
                    nickname = nickname)
        db.session.add(user)
        db.session.commit()
        user.sendConfirmation()

        # login_user(user, remember=form.rememberMe)
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
    response = request.get_json()
    form = LoginForm(response)
    print(response)
    if response['loginAttempts'] >= 3:
        print("HEEEYYY")
        recaptchaResponse = requests.post('https://www.google.com/recaptcha/api/siteverify',
                              data = {'secret' : RECAPTCHA_SECRET_KEY,
                                      'response' : response['recaptcha']})
        print(recaptchaResponse.json(), '2222')
        if not recaptchaResponse.json()['success']:
            print("@@@@@@@")
            return jsonify({'id': -1,
                            'loginAttempts': response['loginAttempts'],
                            'errors': ['Are you human? Then please fill in the reCaptcha!']})
    if form.validate():
        user = User.query.filter_by(email = form.email).first()
        login_user(user, remember=form.rememberMe)
        user.unlock()
        return jsonify({'id': user.id}), 201
    return jsonify(form.response), 201

@app.route('/api/login', methods=['GET'])
def loginApiGet():
    if g.user is not None and g.user.is_authenticated:
        return jsonify({'id': g.user.id}), 201
    user = {'id': '-1',
            'errors': [],
            'RECAPTCHA_SITE_KEY': RECAPTCHA_SITE_KEY,
            'loginAttempts': 0}
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
        email = passwordResetSerializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        email = passwordResetSerializer.loads(token, salt='password-reset-salt')
        user = User.query.filter_by(email = email).first()
        print("HERE FIRST")
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


@app.route('/api/reset/nobodyisgoingtogethere/<email>', methods=['PUT'])
def resetRequest(email):
    if g.user is not None and g.user.is_authenticated:
        print('logged')
        return jsonify({'passed': False})

    form = ResetRequestForm(email)
    if form.validate():
        user = User.query.filter_by(email = email).first()
        if user is None:
            print('does not exist')
            return jsonify({'passed': False})
        user.sendResetEmail()
        print('hello!')
        return jsonify({'passed': True})
    print('not valid')
    return jsonify({'passed': False})



# ##############################################################################
# CONFIRM
# ##############################################################################
@app.route('/confirm/<token>')
def confirm(token):
    return render_template('confirm.html')


@app.route('/api/confirm/<token>', methods=['GET'])
def confirmGet(token):
    if g.user is not None and g.user.is_authenticated:
        return jsonify({'logged': True,
                        'errors': ['You are already logged in.']})
    try:
        passwordResetSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = passwordResetSerializer.loads(token, salt='password-reset-salt', max_age=7200)
    except:
        email = passwordResetSerializer.loads(token, salt='password-reset-salt')
        PendingUsers.query.filter_by(email = email).delete()
        db.session.commit()
        return jsonify({'expired': True})

    user = PendingUsers.query.filter_by(email = email).first()
    print(user)
    if user is None:
        return jsonify({'alreadyConfirmed': True})
    user.migrate(USERPATH)
    print(user)
    PendingUsers.query.filter_by(email = email).delete()
    db.session.commit()
    return jsonify({'confirmation': True})
