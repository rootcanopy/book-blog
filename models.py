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

# AFTER QUITE SOME READING THIS IS THE SIMPLEST WAY TO RUN FLASK-LOGIN WITH PYMONGO
class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)


    @login.user_loader
    def load_user(username):
        u = mongo.db.Users.find_one({"Name": username})
        if not u:
            return None
        return User(username=u['Name'])