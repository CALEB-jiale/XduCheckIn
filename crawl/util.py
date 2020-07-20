# encoding:utf8
import requests
from . import login
from . import get_data
import json
from . import commit


def is_login_success(username, password):
    sess = requests.session()
    login.login(sess, username, password)
    r = get_data.get_data(sess)

    js = json.loads(r.text)
    if '失效' in js['m']:
        return False
    return True


def commit_data(username, password):
    sess = requests.session()
    login.login(sess, username, password)
    res = commit.commit(sess)
    js = json.loads(res.text)
    return js['m']
