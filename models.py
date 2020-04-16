from datetime import datetime
from app import db

class User(db.Document):
    _id = db.ObjectId(primary_key=True)
    username = db.StringField(unique=True)
	email = db.EmailField(unique=True)
    image_file = db.BinaryField(default='default.jpg')
	password = db.StringField(default=True)
    posts = db.relationship('Post', backref='author', lazy=True)
	isAdmin = db.BooleanField(default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Document):
    _id = db.ObjectId(primary_key=True)
    title = db.StringField(required=True,max_length=120)
    date_posted = db.DateTimeField(default=datetime.utcnow)
    content = db.StringField(unique=True)
    user_id = db.ForeignKey('user.id', unique=True)


    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"
