# encoding:utf8

import requests

from . import login


def commit(session):
    headers = {
        'Host': 'xxcapp.xidian.edu.cn',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://xxcapp.xidian.edu.cn',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.14(0x17000e27) NetType/WIFI Language/zh_CN',
        'Connection': 'keep-alive',
        'Referer': 'https://xxcapp.xidian.edu.cn/site/ncov/xidiandailyup',
        'Content-Length': '1835',
    }

    data = {
        'sfzx': '1',
        'tw': '1',
        'area': '陕西省 西安市 长安区',
        'city': '西安市',
        'province': '陕西省',
        'address': '陕西省西安市长安区兴隆街道梧桐大道西安电子科技大学长安校区',
        'geo_api_info': '{"type":"complete","position":{"Q":34.129092068143,"R":108.83138888888902,"lng":108.831389,"lat":34.129092},"location_type":"html5","message":"Get geolocation success.Convert Success.Get address success.","accuracy":65,"isConverted":true,"status":1,"addressComponent":{"citycode":"029","adcode":"610116","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"雷甘路","streetNumber":"266#","country":"中国","province":"陕西省","city":"西安市","district":"长安区","township":"兴隆街道"},"formattedAddress":"陕西省西安市长安区兴隆街道梧桐大道西安电子科技大学长安校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}',
        'sfcyglq': '0',
        'sfyzz': '0',
        'qtqk': '',
        'ymtys': '0'
    }

    response = session.post('https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save',
                            headers=headers, data=data)
    print(response.status_code, response.text)


if __name__ == '__main__':
    sess = requests.session()
    login.login(sess, '', '')
    commit(sess)
