from app import app, db
import os, time, uuid
from string import Template
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
import email.message
import smtplib
import config
from privateData import *
from models import Group, Restaurant, Media, User, UsersInGroups, RestaurantsInGroups

def pr():
    print(2, time.time())
    EM = EmailManager()
    print(3)
    group = Group.query.filter_by(id = 26).first()
    print(4)
    restaurant = Restaurant.query.filter_by(id = 3).first()
    user = User.query.filter_by(id = 1).first()
    print(5)
    # print(EM.buildGroupRestaurantRecommendationTemplate(group, restaurant))
    print(EM.sendAll())
    print(6)



class EmailManager(object):
    def __init__(self):
        self.loadTemplates()


    def readTemplate(self, filename):
        path = os.path.join(os.getcwd(), filename)
        with open(path, 'r') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    def loadTemplates(self):
        self.templateGroup = self.readTemplate('app/templates/groupRestaurantTemplate.html')
        self.templateBody = self.readTemplate('app/templates/recommendation.html')

    def buildGroupRestaurantRecommendationTemplate(self, group, restaurant):
        cidUUID = str(uuid.uuid4())
        template = self.templateGroup.substitute(GROUP_NAME=group.name,
                IMAGE_PATH=cidUUID,
                PATH='http://localhost:5000/group/{}/restaurant/{}'.format(group.id, restaurant.id),
                RESTAURANT_NAME=restaurant.name)
        return template, cidUUID

    def generateSuggestion(self, group):
        # random now
        import numpy as np
        rests = db.session.query(Restaurant).\
                    join(RestaurantsInGroups).filter_by(Group_id = group.id).all()

        if len(rests) > 0:
            return rests[np.random.randint(0, len(rests))]

    def buildUserTemplate(self, user):
        groups = db.session.query(Group).\
                    join(UsersInGroups).filter_by(User_id = user.id).all()
        fullTemplate = ''
        mediaDict = {}
        for group in groups:
            rest = self.generateSuggestion(group)
            if rest is not None:
                template, cidUUID = self.buildGroupRestaurantRecommendationTemplate(group, rest)
                mediaDict[cidUUID] = Media.query.filter_by(id = rest.Media_id).first().mediaPath[3:]
                fullTemplate += template


        fullTemplate = self.templateBody.substitute(
                            NAME=user.nickname,
                            GROUP_TEMPLATE=fullTemplate)
        return fullTemplate, mediaDict

    def sendEmailUser(self, user, server):
        msg = MIMEMultipart('related')

        msg['From'] = MAIL_USERNAME
        msg['To'] = user.email
        msg['Subject'] = 'Test email'
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)
        body, mediaDict = self.buildUserTemplate(user)
        body = MIMEText(body, 'html')
        msgAlternative.attach(body)

        for cidUUID, mediaPath in mediaDict.items():
            with open(os.path.join(os.getcwd() + '/app/', mediaPath), 'rb') as myImage:
                msgImage = MIMEImage(myImage.read())
            msgImage.add_header('Content-ID', '<{}>'.format(cidUUID))
            msg.attach(msgImage)

        # msg.attach(body)
        # msg.add_header('Content-Type', 'text/html')

        server.sendmail(msg['From'], msg['To'], msg.as_string())

        print("!!!", user.email)

    def sendAll(self):
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login( MAIL_USERNAME, MAIL_PASSWORD)

        users = User.query.all()
        for user in users:
            self.sendEmailUser(user, server)
        server.quit()


# t1 = read_template('app/templates/groupRestaurantTemplate.html')
#

#
# t2 = read_template('app/templates/recommendation.html')
# T = t2.substitute(NAME='Marian', GROUP_TEMPLATE = t + t)
