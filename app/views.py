from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .models import Group, UserAvatar, User
from .forms import SignUpForm, LoginForm




@app.before_request
def before_request():
    print('fasole')
    g.user = current_user
    print('fasole2',g.user  )


@lm.user_loader
def load_user(id):
    print(id, "@@@")
    print('mov', User.query.get((id)), str(id))
    return User.query.get((id))


@app.route('/')
@app.route('/home')
def home():
    print(g.user)
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
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
                print(user)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # if request.method == 'GET':
    #     return render_template('login.html', form = form)
    # elif request.method == 'POST':
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        rememberMe = form.rememberMe.data
        login_user(user, remember=rememberMe)
        return redirect(request.args.get('next') or url_for('home'))

    return render_template('login.html',
                            form = form)
        #     user = User.query.filter_by(email = form.email.data).first()
        #     if user is None:
        #         flash("Email not registered! Please Sign Up")
        #         return redirect(url_for('login'))
        #     else:
        #         if user.password != form.password.data:
        #             flash("Wrong Password!")
        #             return redirect(url_for('login'))
        #         else:
        #             rememberMe = False
        #             if 'rememberMe' in session:
        #                 rememberMe = session['rememberMe']
        #                 session.pop('rememberMe', None)
        #             login_user(user, remember = rememberMe)
        #             return redirect(url_for('home'))
        # else:
        #     flash('form not valid')
        #     return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
