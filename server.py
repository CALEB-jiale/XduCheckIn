from flask import Flask, escape, request, render_template, jsonify
import file_util

import flask_sqlalchemy
from crawl import util
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import time
import json
app = Flask("XDU_Check_In")
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'

dir_data = 'data'
db = flask_sqlalchemy.SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    message = db.Column(db.String(64))
    checktime = db.Column(db.Integer)

    def __init__(self, username, message):
        self.username = username
        self.message = message
        self.checktime = int(round(time.time()))


def init():
    file_util.create_dir_if_not_exist(dir_data)
    db.create_all()
    app.config.from_object(APSchedulerJobConfig)

    # 初始化Flask-APScheduler，定时任务
    scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
    scheduler.init_app(app)
    scheduler.start()


@app.route('/api/register', methods=['post'])
def register():
    js = request.get_json(force=True)

    r = util.is_login_success(js['username'], js['password'])
    if not r:
        return json.dumps({"data": '', "message": "Login failed"}, ensure_ascii=False)
    users = User.query.filter_by(username=js['username']).all()
    if len(users) > 0:
        u = users[0]
        u.password = js['password']
        db.session.commit()

    else:
        u = User(js['username'], js['password'])
        db.session.add(u)
        db.session.commit()

    logs = Log.query.filter_by(username=js['username']).all()
    d = []
    for log in logs:
        d.append({"checktime": log.checktime, "message": log.message})
    print(d)
    return json.dumps({"data": d, "message": "Login Success"}, ensure_ascii=False)


@app.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')


@app.route('/index.js', methods=['get'])
def get_js():
    return render_template('index.js')


@app.route('/api/commit', methods=['get'])
def commit_all():
    print('commit')
    users = User.query.all()
    for user in users:
        message = util.commit_data(user.username, user.password)
        log = Log(user.username, message)
        db.session.add(log)
        db.session.commit()
    return 'commit finish'


class APSchedulerJobConfig(object):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    JOBS = [
        {
            'id': 'commit_all',
            'func': commit_all,
            'args': '',
            'trigger': {
                'type': 'cron',
                'day_of_week': "0-6",
                'hour': '6,12,18',
                'minute': '3',
                'second': '0'
            }
        }
    ]


def main():
    init()
    app.run(host='0.0.0.0', port='80')


if __name__ == "__main__":
    main()
