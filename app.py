import os
import env
from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/landing')
def landing():
    return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello {}!</h1>'.format(name)


if __name__ == '__main__':
            app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)