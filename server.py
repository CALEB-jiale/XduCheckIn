from flask import Flask, escape, request
import file_util

import flask_sqlalchemy
from crawl import util
app = Flask("XDU Check In")
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'

dir_data = 'data'


def init():
    file_util.create_dir_if_not_exist(dir_data)


@app.route('/register', methods=['post'])
def register():
    js = request.get_json(force=True)
    u = User(js['username'], js['password'])

    r = util.is_login_success(js['username'], js['password'])
    if not r:
        return 'login failed'
    db.session.add(u)
    db.session.commit()
    return ''


@app.route('/', methods=['get', 'post'])
def index():
    return ''


db = flask_sqlalchemy.SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, username, password):
        self.username = username
        self.password = password


db.create_all()


@app.route('/commit', methods=['get'])
def commit_all():
    print('commit')
    users = User.query.all()
    for user in users:
        util.commit_data(user.username, user.password)
    return 'commit finish'


if __name__ == "__main__":
    init()

    app.run(host='0.0.0.0', port='8080')
