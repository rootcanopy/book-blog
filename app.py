import os
import env
from forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_user import current_user, login_required, UserMixin, login_required
from flask_user.forms import EditUserProfileForm
import bcrypt


app = Flask(__name__)


# SECRET KEY FOR CSRF #TODO
app.config['SECRET_KEY'] = '8bf1555c499fe3cc55021fd1e87585e5'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")


mongo = PyMongo(app)


posts = [
    {
        'author': 'Davie B',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 15th, 2020'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21st, 2020'
    },
]


@app.route('/')
@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/home')
def home():
    return render_template('home.html', posts = posts, title = 'Home-Page')


@app.route('/about')
def about():
    return render_template('about.html', title = 'About-Page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # FUNCTIONALITY OF USER REGISTER
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        
        user = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        
        if existing_user is None:
            # HASHED PW AND INSERT TO COLL
            hashed_pw = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            mongo.db.users.insert({'username': request.form['username'],
                                   'email': request.form['email'],
                                   'password': hashed_pw})
            session['username'] = request.form['username']
            # IF REGISTER IS SUCCESSFUL
            flash(f'Account created for {form.username.data}.. now just to login', 'success')
            return redirect(url_for('login'))#TODO CHANGE TO USER PROFILE

        else:
            flash(f'Registration Failed. Check yo\'self, please try again!', 'danger')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # LOGIN HANDLER
    form = LoginForm()
    if session.get('logged_in'):
        if session['logged_in'] is True:
            return redirect(url_for('home', title='Home'))
     
        user = mongo.db.users.find_one({'email': form.email.data})

        if form.validate_on_submit():
            user = mongo.db.users
            db_user = users.find_one({'email': request.form['email'] })


            if db_user:
                if bcrypt.hashpw(request.form['password'].encode('utf-8'),
                    db_user['password']) == db_user['password']:
                    session['email'] = request.form['email']
                    session['logged_in'] = True
                    session['user_id'] = user_live
                    session['usertype'] = user['type']
            
                return redirect(url_for('home', title='Account'))
        else:
            flash('Login Failed.. Please Check Yourself!', 'danger')
    return render_template('login.html', title = 'Log In', form=form)


@app.route('/account')
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename='images/ + current_user.image_file')
    return render_template('account.html', title='My Account', image_file=image_file, form=form)


@app.route('/logout')
def logout():
    # CLEARS SESH AND REDIRECTS TO HOME
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('home'))


if __name__ == '__main__':
            app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
