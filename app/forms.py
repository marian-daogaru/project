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
