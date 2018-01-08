from app import app, db, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .models import Group, Media, User
from .forms import SignUpForm, LoginForm, EditForm, GroupCreateForm




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



# ##############################################################################
# PROFILE
# ##############################################################################

@app.route('/user/<id>')
@login_required
def user(id, page=1):
    user = User.query.filter_by(id = id).first()
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
    form = EditForm(g.user.nickname)
    print("rosu2")
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.aboutMe = form.aboutMe.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', id=g.user.id))
    elif request.method != "POST":
        form.nickname.data = g.user.nickname
        form.aboutMe.data = g.user.aboutMe
    return render_template('edit.html',
                            form  = form)


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
        nickname = User.make_valid_nickname(nickname)
        user = User(email = form.email.data,
                    password = form.password.data,
                    nickname = nickname,
                    Media_id = avatar.id)
        db.session.add(user)
        db.session.commit()
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
# GROUP CREATE
# ##############################################################################
@app.route('/createGroup', methods=['GET', 'POST'])
@login_required
def createGroup():
    form = GroupCreateForm()

    if form.validate_on_submit():
        avatar = Media(avatarPath = '../static/data/media/avatars/groups/_defautlGroupAvatar.png')
        db.session.add(avatar)
        db.session.commit()

        group = Group(name = form.name.data,
                      aboutGroup = form.aboutGroup.data,
                      Media_id = avatar.id)
        db.session.add(group)
        db.session.commit()

        # REDO THE DB
        # MAKE SO THAT THAT WHEN YOU CREATE A GROUP YOU ARE IN THE GROUP AND YOU BECOME THE ADMIN ALSO
    return redirect(url_for('user', id=g.user.id))


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
