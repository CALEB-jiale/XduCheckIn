from flask import Flask, escape, request, render_template
import file_util

import flask_sqlalchemy
from crawl import util
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask("XDU_Check_In")
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'

dir_data = 'data'
db = flask_sqlalchemy.SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, username, password):
        self.username = username
        self.password = password


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
    u = User(js['username'], js['password'])

    r = util.is_login_success(js['username'], js['password'])
    if not r:
        return 'login failed'
    db.session.add(u)
    db.session.commit()
    return ''


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
        util.commit_data(user.username, user.password)
    return 'commit finish'


class APSchedulerJobConfig(object):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    JOBS = [
        {
            'id': 'commit_all',  # 任务唯一ID
            # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'func': commit_all,
            'args': '',  # 如果function需要参数，就在这里添加
            'trigger': {
                'type': 'cron',  # 类型
                'day_of_week': "0-6",  # 可定义具体哪几天要执行
                'hour': '6,12,18',  # 小时数
                'minute': '3',
                'second': '0'  # "*/3" 表示每3秒执行一次，单独一个"3" 表示每分钟的3秒。现在就是每一分钟的第3秒时循环执行。
            }
        }
    ]


def main():
    init()
    app.run(host='0.0.0.0', port='8080')


if __name__ == "__main__":
    main()
