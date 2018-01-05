from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .models import Group, UserAvatar, User
from .forms import SignUpForm


@lm.user_loader
def load_user(email):
    return User.query.get(email)

@app.before_request
def before_request():
    g.user = current_user



@app.route('/home')
def home():
    return render_template('home.html')


# @app.route('login', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    print("@@@")
    if request.method == 'GET':
        return render_template('signup.html',
                                form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email = form.email.data).first():
                print('albastru')
                flash('Email already registered')
                return redirect(url_for('signup'))
            elif form.password.data != form.confPWD.data:
                print('rosu')
                flash('Password not matching')
                return redirect(url_for('signup'))
            elif User.isValidPassword(form.password.data):
                print('galben')
                flash('!!! Invalid Passwword !!!')
                return redirect(url_for('signup'))
            else:
                print('verde')
                nickname = form.email.data.split('@')[0]
                nickname = User.make_valid_nickname(nickname)
                user = User(email = form.email.data,
                            password = form.password.data,
                            nickname = nickname)
                db.session.add(user)
                db.session.commit()

                rememberMe = False
                if 'rememberMe' in session:
                    rememberMe = session['rememberMe']
                    session.pop('rememberMe', None)
                login_user(user, remember=rememberMe)

            print(form.email.data, form.password.data, form.email.data.split('@'))
            return redirect(request.args.get('next') or url_for('home'))
        else:
            print('portocaliu')
            return redirect(url_for('signup'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
