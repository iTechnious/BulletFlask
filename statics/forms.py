from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import *

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Username')
    email = StringField('E-Mai', validators=[Email()])
    password = PasswordField('Password')
    submit = SubmitField('Submit')
