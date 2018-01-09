import os
from datetime import timedelta
from app import app, db, lm
from config import USERPATH, GROUPPATH, basedir
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .models import Group, Media, User
from .forms import SignUpForm, LoginForm, EditForm, GroupCreateForm,  EditGroupForm
from werkzeug.utils import secure_filename




@app.before_request
def before_request():
    g.user = current_user
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)


@lm.user_loader
def load_user(id):
    print("@@@", id)
    for key in session.keys():
        print("$$$ ", key)
    return User.query.get(int(id))


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
    avatarPath = Media.query.filter_by(id = user.Media_id).first().mediaPath
    groups = g.user.joinedGroups().all()
    groupPaths = []
    for group in groups:
        groupPaths.append(Media.query.filter_by(id = group.Media_id).first().mediaPath)

    # groupPaths = Media.query.join(groups, (groups.Media_id == Media.id)).filter()
    # groupsPath = Media.query.filter_by()
    # print(groupPaths)
    # print("###", dir(groups), type(groups)) #, len(groups), "@@@",  ([group.Media_id for group in groups]), "@@@", dir(Media.id))
    return render_template('profile.html',
                            user = user,
                            avatarPath = avatarPath,
                            zipped = zip(groups, groupPaths))

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    print("rosu2")
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.aboutMe = form.aboutMe.data
        if len(form.password.data) > 0:
            g.user.password = form.password.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your smaller changes have been saved.')

        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash ("No file Selected")
                return redirect(url_for('user', id=g.user.id))

            filename = os.path.join(app.config['USERPATH'], secure_filename(file.filename))
            file.save(os.path.join(basedir + '/app/', filename[3:]))
            flash("It worked!!!! {}".format(filename))
            media = Media.query.filter_by(id = g.user.Media_id).first()
            media.mediaPath = filename
            db.session.add(media)
            db.session.commit()
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
        avatar = Media(mediaPath = USERPATH + '_defautlUserAvatarSmileyFace.png')
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
    session.clear()
    return redirect(url_for('home'))


# ##############################################################################
# GROUP CREATE
# ##############################################################################
@app.route('/createGroup', methods=['GET', 'POST'])
@login_required
def createGroup():
    form = GroupCreateForm()

    if form.validate_on_submit():
        avatar = Media(mediaPath = GROUPPATH + '_defaultGroupAvatar.jpg')
        db.session.add(avatar)
        db.session.commit()

        group = Group(name = form.name.data,
                      aboutGroup = form.aboutGroup.data,
                      Media_id = avatar.id)
        db.session.add(group)
        db.session.commit()

        admin = g.user.joinGroup(g.user, group)
        admin.admin = True
        db.session.add(admin)
        db.session.commit()

        return redirect(url_for('user', id=g.user.id))
        # REDO THE DB
        # MAKE SO THAT THAT WHEN YOU CREATE A GROUP YOU ARE IN THE GROUP AND YOU BECOME THE ADMIN ALSO

    return render_template('createGroup.html',
                            form = form)

# ##############################################################################
# GROUP MANAGEMENT
# ##############################################################################

@app.route('/group/<id>')
@login_required
def group(id):
    group = Group.query.filter_by(id = id).first()

    if group is None:
        flash("Group {} not found.".format(group.name))
        return redirect(url_for('index'))
    avatarPath = Media.query.filter_by(id = group.Media_id).first().mediaPath

    return render_template('group.html',
                            group = group,
                            avatarPath = avatarPath)

@app.route('/group/<id>/edit', methods=['GET', 'POST'])
@login_required
def editGroup(id):
    print("in edit")
    group = Group.query.filter_by(id = id).first()
    if group is None:
        flash("no such group")
        return redirect(url_for('user', id=g.user.id))

    form = EditGroupForm(group.name)
    if form.validate_on_submit():
        group.name = form.name.data
        group.aboutGroup = form.aboutGroup.data

        db.session.add(g.user)
        db.session.commit()

        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash ("No file Selected")
                return redirect(url_for('user', id=g.user.id))

            filename = os.path.join(app.config['GROUPPATH'], secure_filename(file.filename))
            file.save(os.path.join(basedir + '/app/', filename[3:]))
            media = Media.query.filter_by(id = group.Media_id).first()
            media.mediaPath = filename
            db.session.add(media)
            db.session.commit()
        return redirect(url_for('group', id=group.id))
    elif request.method != "POST":
        form.name.data = group.name
        form.aboutGroup.data = group.aboutGroup
    return render_template('editGroup.html',
                            form  = form)

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
