from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length




class LoginForm(FlaskForm):
    email = StringField('email',
                        validators=[DataRequired()],
                        render_kw={"placeholder": "email"})
    password = PasswordField('password',
                        validators=[Length(min=8, max=20)],
                        render_kw={"placeholder": "*****"})
    remember_me = BooleanField('rememberMe',
                                default=False)


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
    remember_me = BooleanField('rememberMe',
                                default=False)
                            
