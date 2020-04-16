import os
from flask_wtf import FlaskForm
from flask_user import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        if username.data != current_user.username:
            user = mongo.db.users.find(username=username.data)
            if user is not None:
                raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        if username.data != current_user.username:
            user = mongo.db.users.find(email=email.data)
            if user is not None:
                raise ValidationError('Email is already taken.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')


    def validate_username(self, username):
        if username.data != current_user.username:
            user = mongo.db.users.find(username=username.data)
            if user is not None:
                raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = mongo.db.users.find(email=email.data)
            if user is not None:
                raise ValidationError('Email is already taken.')
