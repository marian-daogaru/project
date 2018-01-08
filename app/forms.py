from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length
from .models import User



class LoginForm(FlaskForm):
    email = StringField('email',
                        validators=[DataRequired()],
                        render_kw={"placeholder": "email"})
    password = PasswordField('password',
                        validators=[Length(min=8, max=20)],
                        render_kw={"placeholder": "*****"})
    rememberMe = BooleanField('rememberMe',
                                default=False)

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            print("rosu")
            return False
        user = User.query.filter_by(email = self.email.data).first()
        if user is None:
            print('verde')
            self.email.errors.append('Email not registered. Please sign up.')
            return False
        if user.password != self.password.data:
            print('portocaliu')
            self.password.errors.append('Incorrect password!')
            return False
        print('albastru')
        return True



class SignUpForm(FlaskForm):
    email = StringField('email',
                        validators=[DataRequired()],
                        render_kw={"placeholder": "email"})
    password = PasswordField('password',
                        validators=[Length(min=8, max=20)],
                        render_kw={"placeholder": "*****"})
    confPWD = PasswordField('confPWD',
                        validators=[Length(min=8, max=20)],
                        render_kw={"placeholder": "*****"})
    rememberMe = BooleanField('rememberMe',
                                default=False)
