import requests
from . import login
import json


def get_data(session):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://xxcapp.xidian.edu.cn/site/ncov/xidiandailyup',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    response = session.get(
        'https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/index', headers=headers)
    print(response.status_code, response.text)
    return response


def is_login_success(response):
    js = json.loads(response.text)
    if '失效' in js['m']:
        return False
    return True


if __name__ == "__main__":
    sess = requests.session()
    login.login(sess, '', '')
    r = get_data(sess)
    print(is_login_success(r))
