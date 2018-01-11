from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length
from .models import User
import re


class LoginForm(FlaskForm):
    email = StringField('email',
                        validators=[DataRequired()],
                        render_kw={"placeholder": "email"})
    password = PasswordField('password',
                        validators=[Length(min=1, max=20)],
                        render_kw={"placeholder": "*****"})
    rememberMe = BooleanField('rememberMe',
                                default=False)

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        user = User.query.filter_by(email = self.email.data).first()
        if user is None:
            self.email.errors.append('Email not registered. Please sign up.')
            return False
        if user.password != self.password.data:
            self.password.errors.append('Incorrect password!')
            return False
        print('albastru')
        return True


class SignUpForm(FlaskForm):
    email = StringField('email',
                        validators=[DataRequired()],
                        render_kw={"placeholder": "email"})
    password = PasswordField('password',
                        validators=[Length(min=1, max=20)],
                        render_kw={"placeholder": "*****"})
    confPWD = PasswordField('confPWD',
                        validators=[Length(min=1, max=20)],
                        render_kw={"placeholder": "*****"})
    rememberMe = BooleanField('rememberMe',
                                default=False)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if User.query.filter_by(email = self.email.data).first():
            self.email.errors.append('Email already registered')
            return False
        if self.password.data != self.confPWD.data:
            self.confPWD.errors.append('Password not matching')
            return False
        if User.isValidPassword(self.password.data):
            self.password.errors.append('!!! Invalid Passwword !!!')
            return False
        return True

class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    aboutMe = TextAreaField('aboutMe', validators=[Length(min=0, max=200)])
    password = PasswordField('password',
        render_kw={"placeholder": "*****"})
    confPWD = PasswordField('confPWD',
        render_kw={"placeholder": "*****"})

    def __init__(self, original_nickname, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not FlaskForm.validate(self):
            print("rosu")
            return False
        if self.nickname.data == self.original_nickname:
            print("verde")
            return True
        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            print("mov")
            self.nickname.errors.append(gettext('This nickname has invalid characters. Please use letters, numbers, dots and underscores only.'))
            return False
        if self.password.data != self.confPWD.data:
            self.confPWD.errors.append('Password not matching')
            return False
        if User.isValidPassword(self.password.data):
            self.password.errors.append('!!! Invalid Passwword !!!')
            return False
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
