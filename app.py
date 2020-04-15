import os
import env
from flask import Flask, render_template, redirect, url_for, flash, request, session
from forms import RegistrationForm, LoginForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import bcrypt
from flask_login import login_user, logout_user, login_required


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
    # FUNCTIONALITY OF USER SIGN UP
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        
        if existing_user is None:
            # HASHED PW AND INSERT TO COLL
            hashed_pw = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username': request.form['username'],
                                'email': request.form['email'],
                                'password': hashed_pw})
            session['username'] = request.form['username']
            # IF REGISTER IS SUCCESSFUL
            flash(f'Account created for {form.username.data}.. now just to login', 'success')
            return redirect(url_for('login'))#TODO CHANGE TO USER PROFILE

        else:
            flash(f'Registration Failed. Check yo\'self, please try again!', 'danger')
            return render_template('register.html', title='Register', form=form)

    return render_template('register.html', title = 'Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # LOGIN HANDLER
    if session.get('logged_in'):
        if session['logged_in'] is True:
            return redirect(url_for('home', title='Home'))
     
    form = LoginForm()
    user = mongo.db.users.find_one({'email': form.email.data})

    if form.validate_on_submit():
        users = mongo.db.users
        db_user = users.find_one({'email': request.form['email'] })

        if db_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'),
                db_user['password']) == db_user['password']:
                session['email'] = request.form['email']
                session['logged_in'] = True
        return redirect(url_for('home', title='Signed In', form=form))
    else:
        flash('Login Failed.. Please Check Yourself!', 'danger')
    return render_template('login.html', title = 'Log In', form=form)

""""
@app.route('/user/<username>')
def user(username):
    user = mongo.db.users.find_one('username': request.username.data)
    return render_template('user.html', user=user)
"""

def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    # CLEARS SESH AND REDIRECTS TO HOME
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
            app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)