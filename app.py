import os
import env
from flask import Flask, render_template

app = Flask(__name__)

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
@app.route('/landing')
def landing():
    return render_template('home.html', posts = posts)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
            app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)