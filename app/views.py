from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .models import Group, Media, User
from .forms import SignUpForm, LoginForm




@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get((id))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/user/<nickname>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    avatarPath = Media.query.filter_by(id = user.Media_id).first().avatarPath
    return render_template('profile.html',
                            user = user,
                            avatarPath = avatarPath)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    return render_template('edit.html')

# ##############################################################################
# LOGIN / SIGNUP
# ##############################################################################
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
    if form.validate_on_submit():
        avatar = Media(avatarPath = '../static/data/media/avatars/users/_defautlUserAvatarSmileyFace.png')
        db.session.add(avatar)
        db.session.commit()

        nickname = form.email.data.split('@')[0]
        print(nickname, "verde")
        nickname = User.make_valid_nickname(nickname)
        user = User(email = form.email.data,
                    password = form.password.data,
                    nickname = nickname,
                    Media_id = avatar.id)
        db.session.add(user)
        db.session.commit()
        print(nickname, 'abastru')
        rememberMe = form.rememberMe.data
        login_user(user, remember=rememberMe)
        return redirect(request.args.get('next') or url_for('home'))
    return render_template('signup.html',
                            form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        rememberMe = form.rememberMe.data
        login_user(user, remember=rememberMe)
        return redirect(request.args.get('next') or url_for('home'))

    return render_template('login.html',
                            form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



# ##############################################################################
# ERROR HANDLING
# ##############################################################################
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
