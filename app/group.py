import os
import uuid
import numpy as np
from app import app, db, lm
from config import GROUPPATH, basedir
from flask import render_template, session, request, g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .models import Group, Media, User, UsersInGroups, RestaurantsInGroups, Restaurant, PendingUsersInGroups, RestaurantDetails
from .forms import GroupCreateForm,  EditGroupForm, PeopleGroupForm
from werkzeug.utils import secure_filename

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

# ##############################################################################
# PROFILE GROUPS
# ##############################################################################
@app.route('/user/<id>/groups')
@login_required
def userGroups(id):
    return render_template('groupsUser.html')

@app.route('/api/user/<int:id>/groups', methods=['GET'])
@login_required
def userGroupsGet(id):
    user = User.query.filter_by(id = id).first()
    if user is not None and g.user.is_authenticated:
        groups = user.joinedGroups()
        user = row2dict(user)
        user.pop('password')
        user.pop('email')
        allGroups = []
        for group in groups:
            mediaPath = Media.query.filter_by(id = group.Media_id).first().mediaPath
            group = row2dict(group)
            group['mediaPath'] = mediaPath
            allGroups.append(group)
        output = {'user': user,
                    'groups': allGroups}

        if g.user.id != id:
            output['userLocal'] = row2dict(g.user)
        return jsonify(output)
    return jsonify({'accessDenied': True})



# ##############################################################################
# GROUP CREATE
# ##############################################################################
@app.route('/createGroup')
@login_required
def createGroup():
    return render_template('createGroup.html')

@app.route('/api/createGroup', methods=['GET'])
@login_required
def createGroupGet():
    return jsonify(row2dict(g.user))

@app.route('/api/createGroup', methods=['POST'])
@login_required
def createGroupPost():
    response = request.get_json()
    form = GroupCreateForm(response)

    if form.validate():
        avatar = Media(mediaPath = GROUPPATH + '_defaultGroupAvatar.jpg')
        db.session.add(avatar)
        db.session.commit()

        group = Group(name = form.name,
                      aboutGroup = form.aboutGroup,
                      Media_id = avatar.id)
        db.session.add(group)
        db.session.commit()

        admin = g.user.joinGroup(g.user, group)
        admin.admin = True
        db.session.add(admin)
        db.session.commit()

        return jsonify({'created': True,
                        'groupID' : group.id})

    return jsonify({'created': False,
                    'errors': form.errors})

# ##############################################################################
# GROUP MANAGEMENT
# ##############################################################################
@app.route('/group/<id>')
@login_required
def group(id):
    return render_template('group.html')


@app.route('/api/group/<id>', methods=['GET'])
@login_required
def groupApiGet(id):
    # get group
    group = Group.query.filter_by(id = eval(id)).first()
    if group is None:
        flash("Group {} not found.".format(group.name))
        return jsonify({'id': -1,
                        'errors': ['No such group.']})
    # data that is easier to get now, or cannot be obtained after this is a dict
    users = group.users()
    pending = len(group.pendingRestaurants()) + len(group.pendingUsers())
    restaurants = group.restaurants()
    suggested = group.suggestedRestaurant()
    inGroup = g.user.isInGroup(g.user, group)  # do this before we change group
    # make group a dict to be jsonified
    group = row2dict(group)
    group['userID'] = g.user.id
    group['mediaPath'] = Media.query.filter_by(id = group["Media_id"]).first().mediaPath
    if inGroup:
        group['isAdmin'] = g.user.isAdmin(group['id'])
    group['inGroup'] = inGroup
    group['pending'] = pending
    # get all users in the group
    group['users'] = []
    for user in users:
        user = row2dict(user)
        group['users'].append(user)
    # get all restaurants in the group
    group['restaurants'] = []
    for restaurant in restaurants:
        mediaPath = restaurant.mediaPath()
        userRating = restaurant.currentUserRating(g.user)
        rating = restaurant.groupRating(group['id'])
        restaurant = row2dict(restaurant)
        restaurant['mediaPath'] = mediaPath
        restaurant['rating'] = rating
        restaurant['userRating'] = userRating
        details = RestaurantDetails.query.filter_by(Restaurant_id = restaurant['id']).first()
        if details is not None:
            restaurant['lon'] = details.lon
            restaurant['lat'] = details.lat
        group['restaurants'].append(restaurant)
    # todays recommendation
    if suggested is not None:
        rating = suggested.groupRating(group['id'])
        suggested = row2dict(suggested)
        suggested['mediaPath'] = Media.query.filter_by(id = suggested["Media_id"]).first().mediaPath
        suggested['rating'] = rating
        group['suggestedRestaurant'] = suggested
    else:
        group['suggestedRestaurant'] = False

    return jsonify(group)

@app.route('/api/group/<id>', methods=['POST'])
@login_required
def groupApiPost(id):
    response = request.get_json()
    print(response)
    if 'emails' in response.keys():
        if len(response['emails']) > 0:
            form = PeopleGroupForm(response)

            if form.validate():
                group = Group.query.filter_by(id = eval(id)).first()
                if g.user.isAdmin(group.id):
                    print("Group added bacause admin!")
                    return AddPeopletoGroup(form.emails, group)
                else:
                    print("Group !added bacause !admin!")
                    return AddPeopletoPending(form.emails, group)

        return jsonify({'errors': form.errors}), 201
    return ({'errors': ['Not a valid post form!']}), 400


# #############################################################################
# Restaurant Feedback
# #############################################################################
@app.route('/api/group/<id>/<ids>', methods=['PUT'])
@login_required
def groupApiPut(id, ids):
    """
        ids = [userID, restaurantID, rating]
        userID is checked so we can verify if the user actually is in the group
    """
    group = Group.query.filter_by(id = id).first()
    ids = ids.split(',')
    if g.user.id == int(ids[0]):
        if g.user.isInGroup(g.user, group):
            g.user.rateRestaurant(ids[1], ids[2])
            restaurant = Restaurant.query.filter_by(id = int(ids[1])).first()
            rating = restaurant.groupRating(group.id)
            return jsonify({"rated": True,
                            'rating': rating})
        return jsonify({'accessDenied': True})
    return jsonify({'accessDenied': True})


@app.route('/api/group/<id>/<ids>', methods=['DELETE'])
@login_required
def groupApiDeleteRestaurant(id, ids):
    """
        ids = [userID, restaurantID]
        userID is checked so we can verify if the user actually is in the group
    """
    print(ids)
    group = Group.query.filter_by(id = id).first()
    ids = ids.split(',')
    if g.user.id == int(ids[0]):
        if g.user.isAdmin(group.id):
            g.user.rateRestaurant(ids[1], 0)
            return jsonify({"confirmation": "You rated the restaurant negatively, therefore it was removed from this group."})
        return jsonify({'accessDenied': True})
    return jsonify({'accessDenied': True})


# #############################################################################
# User Managemenet
# #############################################################################
def AddPeopletoGroup(emails, group):
    # emails must be a list
    for email in emails:
        user = User.query.filter_by(email = email).first()
        print(user)
        if user is None:
            print('here')
            return jsonify({'errors': ["The email {} is not registered!".format(email)]}), 201
        else:
            user.joinGroup(user, group)
    # because we are adding new ppl, the ratings must be recalculated
    restaurants = group.restaurants()
    for restaurant in restaurants:
        restaurant.assignNewGroupRating(group)
    return jsonify({'added': 'All people were added succesfully to this group.'}), 201

def AddPeopletoPending(emails, group):
    # emails must be a list
    for email in emails:
        user = User.query.filter_by(email = email).first()
        print(user, "!!!")
        if user is None:
            print('here')
            return jsonify({'errors': ["The email {} is not registered!".format(email)]}), 201
        else:
            # print(user, '###')
            PendingUsersInGroups.addPendingUser(user, group)
    group.emailAdminsUpdate()
    return jsonify({'added': 'All people were added succesfully to this group. Awaiting admin approval.'}), 201


@app.route('/api/group/leave', methods=['POST'])
@login_required
def leaveGroup():
    data = request.get_json()
    group = group = Group.query.filter_by(id = data['groupID']).first()
    if g.user.isInGroup(g.user, group):
        print("hello", group.lastAdmin())
        lastAdmin = group.lastAdmin()
        if (lastAdmin and data['consent'] == 1):
            g.user.leaveGroup(g.user, group)
            deleteGroup(group.id)
            return jsonify({'left': True,
                            'id': g.user.id})
        elif not lastAdmin:
            g.user.leaveGroup(g.user, group)
            return jsonify({'left': True,
                            'id': g.user.id})
        else:
            return jsonify({'left': False,
                            'lastAdmin': True})

    return jsonify({'left': False})

# ##############################################################################
# DELETE GROUP
# ##############################################################################
@app.route('/api/group/<id>/delete', methods=['DELETE'])
@login_required
def deleteGroup(id):
    group = Group.query.filter_by(id = id).first()
    Media_id = group.Media_id
    mediaID = group.Media_id  # because of how the FK work, group will be delete first, then media. so if we dont store it, Media_id will be gone...
    UsersInGroups.query.filter_by(Group_id = group.id).delete()  # remove all records of all the users in that group
    RestaurantsInGroups.query.filter_by(Group_id = group.id).delete()  # remove all the restaurant from this group
    Group.query.filter_by(id = group.id).delete()  # remove the group
    Media.query.filter_by(id = Media_id).delete()  # remove the media part
    db.session.commit()
    return jsonify({"deleted": True,
                    'id': g.user.id})


# ##############################################################################
# EDIT GROUP
# ##############################################################################
@app.route('/group/<id>/edit')
@login_required
def editGroup(id):
    return render_template('editGroup.html')

@app.route('/api/group/<id>/edit', methods=['GET'])
@login_required
def editGroupGet(id):
    group = Group.query.filter_by(id = id).first()
    if g.user.isInGroup(g.user, group) and g.user.isAdmin(group.id):
        users = group.users()
        pendingUsers = len(group.pendingUsers())
        pendingRestaurants = len(group.pendingRestaurants())
        group = row2dict(group)
        group['pendingUsers'] = pendingUsers
        group['pendingRestaurants'] = pendingRestaurants
        group['mediaPath'] = Media.query.filter_by(id = group["Media_id"]).first().mediaPath
        group['users'] = []
        for user in users:
            # user = User.query.filter_by(id = user["User_id"]).first()
            user = User.query.filter_by(id = user.User_id).first()
            isAdmin = user.isAdmin(group['id'])
            user = row2dict(user)
            print(user)
            user['mediaPath'] = Media.query.filter_by(id = user['Media_id']).first().mediaPath
            user['isAdmin'] = isAdmin
            group['users'].append(user)
        return jsonify(group)
    else:
        return jsonify({'accessDenied': True})

@app.route('/api/group/<id>/edit', methods=['POST'])
@login_required
def editGroupPost(id):
    response = request.get_json()
    group = Group.query.filter_by(id = id).first()
    form = EditGroupForm(response)
    if form.validate():
        group.name = form.name
        group.aboutGroup = form.aboutGroup

        db.session.add(group)
        db.session.commit()
        if len(response['avatar']) > 0:
            avatar = response['avatar'].split(',')[1]

            filename = str(uuid.uuid4().hex) + '.png'
            filename = os.path.join(app.config['GROUPPATH'], secure_filename(filename))
            with open(os.path.join(basedir + '/app/', filename[3:]), 'w') as myImage:
                # missing_padding = len(form.avatar) % 4
                # if missing_padding != 0:
                #     form.avatar += b'='* (4 - missing_padding)
                myImage.write(avatar.decode('base64'))
            media = Media.query.filter_by(id = group.Media_id).first()
            media.mediaPath = filename
            db.session.add(media)
            db.session.commit()

        for newAdminID in response['ids']:
            group.makeAdmin(newAdminID)

        return jsonify({'updated': True})
    return jsonify({'errors': form.errors})

@app.route('/api/group/-1/edit/<ids>', methods=['DELETE'])
@login_required
def editGroupDelete(ids):
    # first ID will be group ID, the remaining will be the ids of the ppl to removed
    ids = np.array(ids.split(",")).astype(int)
    group = group = Group.query.filter_by(id = ids[0]).first()
    if ids.size > 1:
        for userID in ids[1:]:
            user = User.query.filter_by(id = userID).first()
            user.leaveGroup(user, group)
        return jsonify({'removed': True})
    return jsonify({'removed': False})
