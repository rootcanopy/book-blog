import os
import env
from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '8bf1555c499fe3cc55021fd1e87585e5'

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


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title = 'Register', form = form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Log In', form = form)


if __name__ == '__main__':
            app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)