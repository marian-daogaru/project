import os
from datetime import timedelta
import uuid
from app import app, db, lm
from config import USERPATH, GROUPPATH, basedir
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .models import Group, Media, User, UsersInGroups
from .forms import SignUpForm, LoginForm, EditForm, GroupCreateForm,  EditGroupForm, PeopleGroupForm
from werkzeug.utils import secure_filename
import json

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/api/home', methods=['GET'])
def homeApi():
    if not g.user.is_authenticated:  # user not loggedin
        user = g.user.__dict__
        user['id'] = "-1"
    else:
        user = row2dict(g.user)
    return jsonify(user)

# ##############################################################################
# PROFILE
# ##############################################################################

@app.route('/user/<int:id>')
@login_required
def user(id, page=1):
    return render_template('profile.html')

@app.route('/api/user/<int:id>', methods=['GET'])
@login_required
def userApi(id, page=1):
    user = User.query.filter_by(id = id).first()
    if user is None:
        flash('User {} not found.'.format(id))
        return redirect(url_for('index'))
    # flash(groupID)

    groups = user.joinedGroups().all()
    user = row2dict(user)
    user['avatar'] = row2dict(Media.query.filter_by(id = user["Media_id"]).first())
    user['Group'] = []
    for group in groups:
        group = row2dict(group)
        group['Media'] = row2dict(Media.query.filter_by(id = group["Media_id"]).first())
        user['Group'].append(group)

    return jsonify(user)



# ##############################################################################
# EDIT
# ##############################################################################
@app.route('/edit')
@login_required
def edit():
    return render_template('edit.html')

@app.route('/api/edit', methods=['GET'])
@login_required
def editApiGet():
    if g.user is not None and g.user.is_authenticated:
        return jsonify({'nickname': g.user.nickname,
                        'aboutMe': g.user.aboutMe}), 201
    user = {'id': '-1',
            'errors': []}
    return jsonify(user), 201

@app.route('/api/edit', methods=['POST'])
@login_required
def editApiPost():
    form = EditForm(request.get_json())
    if form.validate():
        g.user.nickname = form.nickname
        g.user.aboutMe = form.aboutMe
        if len(form.password) > 0:  # it was already checked in validate
            g.user.password = form.password
        db.session.add(g.user)
        db.session.commit()

        if len(form.avatar) > 0:
            form.avatar = form.avatar.split(',')[1]
            print("hello", dir(form.avatar), len(form.avatar))

            filename = str(uuid.uuid4().hex) + '.png'
            filename = os.path.join(app.config['USERPATH'], secure_filename(filename))
            print(filename)
            with open(os.path.join(basedir + '/app/', filename[3:]), 'w') as myImage:
                # missing_padding = len(form.avatar) % 4
                # if missing_padding != 0:
                #     form.avatar += b'='* (4 - missing_padding)
                myImage.write(form.avatar.decode('base64'))
            media = Media.query.filter_by(id = g.user.Media_id).first()
            media.mediaPath = filename
            db.session.add(media)
            db.session.commit()
        return jsonify({'nickname': g.user.nickname,
                        'aboutMe': g.user.aboutMe,
                        'id': g.user.id}), 201
    print(form.errors)
    return jsonify({'id': -1,
                    'errors': form.errors}), 201

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
    print("in logout")
    logout_user()
    session.clear()
    print(g.user, current_user)
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
    group = Group.query.filter_by(id = eval(id)).first()
    if group is None:
        flash("Group {} not found.".format(group.name))
        return redirect(url_for('index'))
    form = PeopleGroupForm()
    avatarPath = Media.query.filter_by(id = group.Media_id).first().mediaPath

    if form.validate_on_submit():
        print("after Validate")
        valid, emails = form.validateCorrectEmails()
        AddPeopletoGroup(emails, group)
        flash("Flash everyone was added successfully!")
    print("outside if")
    print(request.form, "###")
    # return jsonify({})
    return render_template('group.html',
                            group = group,
                            avatarPath = avatarPath,
                            form = form)

@app.route('/api/group/<id>', methods=['GET'])
@login_required
def groupApiGet(id):
    group = Group.query.filter_by(id = eval(id)).first()
    if group is None:
        flash("Group {} not found.".format(group.name))
        return jsonify({'id': -1,
                        'errors': ['No such group.']})
    users = group.users()
    inGroup = g.user.isInGroup(g.user, group)  # do this before we change group
    print("222", inGroup, users)
    group = row2dict(group)
    group['mediaPath'] = Media.query.filter_by(id = group["Media_id"]).first().mediaPath
    if inGroup:
        group['isAdmin'] = g.user.isAdmin(group['id'])
    group['inGroup'] = inGroup
    group['users'] = []
    for user in users:
        user = row2dict(user)
        group['users'].append(user)
    return jsonify(group)

@app.route('/api/group/<id>', methods=['POST'])
@login_required
def groupApiPost(id):
    testDict = {'hello': 'this works'}
    print("in POST")
    form = PeopleGroupForm()
    return jsonify(dict(form))



        # user = User.query.filter_by(id = id).first()
        # if user is None:
        #     flash('User {} not found.'.format(id))
        #     return redirect(url_for('index'))
        # # flash(groupID)
        # if 'groupIDDelete' in request.args:
        #     groupID = request.args['groupIDDelete']
        #     flash("was here")
        #     deleteGroup(groupID)
        #
        # groups = user.joinedGroups().all()
        # user = row2dict(user)
        # user['avatar'] = row2dict(Media.query.filter_by(id = user["Media_id"]).first())
        # user['Group'] = []
        # for group in groups:
        #     group = row2dict(group)
        #     group['Media'] = row2dict(Media.query.filter_by(id = group["Media_id"]).first())
        #     user['Group'].append(group)

@app.route('/api/group/leave', methods=['POST'])
@login_required
def leaveGroup():
    data = request.get_json()
    group = group = Group.query.filter_by(id = data['groupID']).first()
    if g.user.isInGroup(g.user, group):
        print("hello")
        g.user.leaveGroup(g.user, group)
        return jsonify({'left': True})
    print("not hello")
    return jsonify({'left': False})


@app.route('/group/<id>/edit', methods=['GET', 'POST'])
@login_required
def editGroup(id):
    print("in edit", dir(app))
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

@app.route('/api/group/<id>/delete', methods=['POST'])
@login_required
def deleteGroup(id):
    group = Group.query.filter_by(id = id).first()
    if group is None:
        flash("No such group")
        return render_template(url_for('home'))

    mediaID = group.Media_id  # because of how the FK work, group will be delete first, then media. so if we dont store it, Media_id will be gone...
    UsersInGroups.query.filter_by(Group_id = group.id).delete()  # remove all records of all the users in that group
    # add the Restaurants in Groups when implemented
    Group.query.filter_by(id = groupID).delete()  # remove the group
    Media.query.filter_by(id = group.Media_id).delete()  # remove the media part
    db.session.commit()
    flash("Group Successfully deleted!")

def AddPeopletoGroup(emails, group):
    # emails must be a list
    for email in emails:
        user = User.query.filter_by(email = email).first()
        if user is None:
            flash("The email {} is not registered!".format(email))
        else:
            user.joinGroup(user, group)


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
