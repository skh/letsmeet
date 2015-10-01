from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField

class LoginForm(Form):
    email = StringField('Email')
    password = PasswordField('Password')
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')