import os
import uuid
import numpy as np
from app import app, db, lm
from config import USERPATH, basedir
from flask import redirect, render_template, session, request, g, jsonify, flash, redirect
from flask_login import login_required
from .models import Media, User, Group
from .forms import EditForm
from werkzeug.utils import secure_filename

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

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

    if g.user.id == user.id:
        groups = user.adminOfGroups()
        user = row2dict(user)
        user['avatar'] = row2dict(Media.query.filter_by(id = user["Media_id"]).first())
        user['Group'] = []
        for group in groups:
            group = row2dict(group)
            group['Media'] = row2dict(Media.query.filter_by(id = group["Media_id"]).first())
            user['Group'].append(group)
        return jsonify(user)
    else:
        return jsonify({'accessDenied': True})


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
        print(g.user.aboutMe, 'aboutmeeeee')
        if len(form.password) > 0:  # it was already checked in validate
            g.user.password = form.password
        db.session.add(g.user)
        db.session.commit()

        if len(form.avatar) > 0:
            form.avatar = form.avatar.split(',')[1]

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
# PENDING USERS
# ##############################################################################
@app.route('/group/<id>/edit/pendingUsers')
@login_required
def editPendingUsers(id):
    return render_template('pendingUsers.html')

@app.route('/api/group/<id>/edit/pendingUsers', methods=['GET'])
@login_required
def editPendingUsersGet(id):
    group = Group.query.filter_by(id = id).first()
    if g.user.isInGroup(g.user, group) and g.user.isAdmin(group.id):
        pendingUsers = group.pendingUsers()
        pendingMedia = group.pendingUsersMedia()
        print(pendingUsers, pendingMedia, "@@@")
        users = []
        for user, mediaPath in zip(pendingUsers, pendingMedia):
            user = row2dict(user)
            user['mediaPath'] = mediaPath
            user.pop('password')
            users.append(user)
        print(users)
        return jsonify({'users': users,
                        'groupID': group.id})
    return jsonify({'accessDenied': True})

@app.route('/api/group/<id>/edit/pendingUsers/<ids>', methods=['PUT'])
@login_required
def editPendingUsersPut(id, ids):
    group = Group.query.filter_by(id = id).first()
    print(ids, len(ids), "@@@")
    if len(ids) == 0:
        return jsonify({'errors': ['No users!']})
    if g.user.isInGroup(g.user, group) and g.user.isAdmin(group.id):
        ids = np.array(ids.split(',')).astype(int)
        group.addPendingUsers(ids)
        return jsonify({'confirmations': ['Users added succesfully.']})
    return jsonify({'accessDenied': True})

@app.route('/api/group/<id>/edit/pendingUsers/<ids>', methods=['DELETE'])
@login_required
def editPendingUsersDelte(id, ids):
    group = Group.query.filter_by(id = id).first()
    print(ids, len(ids), "@@@ REMOVE")
    if len(ids) == 0:
        return jsonify({'errors': ['No users!']})
    if g.user.isInGroup(g.user, group) and g.user.isAdmin(group.id):
        ids = np.array(ids.split(',')).astype(int)
        group.removePendingUsers(ids)
        return jsonify({'confirmations': ['Users removed succesfully.']})
    return jsonify({'accessDenied': True})
