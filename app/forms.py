from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length
from .models import User
import re


class LoginForm(object):
    def __init__(self, inputDict, *args, **kwargs):
        self.email = inputDict['email']
        self.password = inputDict['password']
        self.rememberMe = inputDict['rememberMe']
        self.errors = []

    def validate(self):
        """email check for @ is done by bootstrap.
        length is also checked, but not an issue if we double check"""
        if len(self.email) ==  0 or len(self.password) == 0:
            print("rosu")
            self.errors.append("Missing field.")
            return False
        user = User.query.filter_by(email = self.email).first()
        if user is None:
            self.errors.append("Invalid username / password.")
            print("galben")
            return False
        if user.password != self.password:
            self.errors.append("Invalid username / password.")
            print("portocaliu")
            return False
        print('albastru')
        return True


class SignUpForm():
    def __init__(self, inputDict, *args, **kwargs):
        self.email = inputDict['email']
        self.password = inputDict['password']
        self.confpwd = inputDict['confpwd']
        self.rememberMe = inputDict['rememberMe']
        self.errors = []

    def validate(self):
        """email check for @ is done by bootstrap.
        length is also checked, but not an issue if we double check"""
        if len(self.email) ==  0 or len(self.password) == 0 or len(self.confpwd) == 0:
            print("rosu")
            self.errors.append("Missing field.")
            return False
        if User.query.filter_by(email = self.email).first():
            print("galben")
            self.errors.append('Email already registered')
            return False
        if len(self.email) > 30:
            print("beige 22")
            self.errors.append("Email too long.")
            return False
        if len(self.password) > 20 or len(self.password) < 8:
            print("beige")
            self.errors.append("Password not the right dimension. It must be between 8 and 20 chracters long.")
            return False
        if self.password != self.confpwd:
            print("portocaliu")
            self.errors.append('Password not matching')
            return False
        if User.isValidPassword(self.password):
            print("maro")
            self.errors.append('Invalid Passwword.')
            return False
        return True

class EditForm():
    def __init__(self, inputDict, *args, **kwargs):
        self.nickname = inputDict['nickname']
        self.aboutMe = inputDict['aboutMe']
        self.password = inputDict['password']
        self.confpwd =  inputDict['confpwd']
        self.avatar = inputDict['avatar']
        self.errors = []

    def validate(self):
        if len(self.nickname) ==  0:
            print("rosu")
            self.errors.append("Nickname must be present.")
            return False
        if len(self.nickname) > 30:
            print("rosu 2")
            self.errors.append("Nickname too large.")
            return False
        if self.nickname != User.make_valid_nickname(self.nickname):
            print("mov")
            self.errors.append('This nickname has invalid characters. Please use letters, numbers, dots and underscores only.')
            return False
        if len(self.password) > 0:
            if self.password != self.confpwd:
                self.errors.append('Password not matching')
                return False
            if len(self.password) > 20 or len(self.password) < 8:
                print("beige")
                self.errors.append("Password not the right dimension. It must be between 8 and 20 chracters long.")
                return False
            if self.password != self.confpwd:
                print("portocaliu")
                self.errors.append('Password not matching')
                return False
            if User.isValidPassword(self.password):
                print("maro")
                self.errors.append('Invalid Passwword.')
                return False
        # must do something about the aboutMe, to check it is not injecting stuff
        return True

# ##############################################################################
# GROUP Forms
# ##############################################################################
class GroupCreateForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    aboutGroup = TextAreaField('aboutGroup', validators=[Length(min=0, max=200)])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        return True

class EditGroupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    aboutGroup = TextAreaField('aboutGroup', validators=[Length(min=0, max=200)])

    def __init__(self, original_name, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_name = original_name

    def validate(self):
        if not FlaskForm.validate(self):
            print("rosu")
            return False
        if self.name.data == self.original_name:
            print("verde")
            return True
        if self.name.data != User.make_valid_nickname(self.name.data):
            print("mov")
            self.name.errors.append(gettext('This nickname has invalid characters. Please use letters, numbers, dots and underscores only.'))
            return False
        return True

class PeopleGroupForm(FlaskForm):
    emails = TextAreaField('emails',
                            validators=[Length(max=1000)])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        comp = re.compile(r"^[-A-Za-z0-9_\s\.,@]*$")
        print("!!!!", bool(comp.match(self.emails.data)))
        print(self.validateCorrectEmails(), "!!!!")
        if not bool(comp.match(self.emails.data)):
            self.emails.errors.append("The field contains characters that are not permitted. \n ")
            self.emails.errors.append("The only permitted characters are Letters, Numbers, '@', Space, '_', '-', '.', ','.")
            return False
        isValid, emails = self.validateCorrectEmails()
        if not isValid:
            self.emails.errors.append("This is not correct: {}".format(self.validateCorrectEmails()[1]))
            return False
        return True

    def validateCorrectEmails(self):
        text = self.emails.data
        text = text.replace(",", " ")
        emails = text.split()
        if len(emails) == 0:
            return True, []

        for email in emails:
            if "@" not in email:
                return False, [email]
            parts = email.split("@")
            if "." not in parts[1]:
                return False, [email]
            if len(parts[1].split('.')[0]) == 0:
                return False, [email]

        return True, emails
