

# AFTER QUITE SOME READING THIS IS THE SIMPLEST WAY TO RUN FLASK-LOGIN WITH PYMONGO
class user:
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