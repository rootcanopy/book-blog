import os
from flask_login import login_manager, current_user, UserMixin
from datetime import datetime
from flask_login.login_manager import LoginManager
from wtforms.fields.core import IntegerField, StringField
from wtforms.fields.simple import BooleanField
from django.db.models.fields import EmailField
from twisted.protocols.amp import Integer
from django.forms.fields import DateTimeField
from django.db.models import ForeignKey
from xml.dom.minidom import Text
from click.types import DateTime
from flask import app


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.find(user_id)


class User(db.Document, UserMixen):
    id = IntegerField(primary_key=True)
    username = StringField(unique=True)
    email = EmailField(unique=True)
    image_file = StringField(default='default.jpg')
    password = StringField(default=True)
    isAdmin = BooleanField(default=False)
    posts = Relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Document):
    id = Integer(primary_key=True)
    title = StringField(required=True)
    date_posted = DateTime(nullable=False, default=datetime.utcnow())
    content = StringField(Text, nullable=False)
    last_updated = DateTimeField(default=datetime.datetime.now())
    user_id = Integer(ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
