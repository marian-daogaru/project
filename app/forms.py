from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length
from .models import User



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


# class PasswordInput(Input):
#     """
#     Render a password input.
#
#     For security purposes, this field will not reproduce the value on a form
#     submit by default. To have the value filled in, set `hide_value` to
#     `False`.
#     """
#     input_type = 'password'
#
#     def __init__(self, hide_value=True):
#         self.hide_value = hide_value
#
#     def __call__(self, field, **kwargs):
#         if self.hide_value:
#             kwargs['value'] = ''
#         return super()

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


class GroupCreateForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    aboutGroup = TextAreaField('aboutGroup', validators=[Length(min=0, max=200)])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        return True
