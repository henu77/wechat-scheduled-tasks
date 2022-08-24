from datetime import date, datetime
import math
from turtle import color
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import yaml
# 获取配置文件绝对路径
yaml_path = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "config.yaml")

# 读取配置文件


def read_yaml_all():
    try:
        # 打开文件
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except:
        return None


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) +
                             "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


def getWeek():
    return week_list[today.isoweekday()-1]


def getWeather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['low']), math.floor(weather['high']), weather['date']


config = read_yaml_all()
config = config['data']
# 参数
today = datetime.now()
start_date = config['start_date']
city = config['city']
birthday = config['birthday']


app_id = config['app_id']
app_secret = config['app_secret']

user_id = config['user_id']
template_id = config['template_id']


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather, low, high, today2 = getWeather()
low = str(low)+" ℃"
high = str(high)+" ℃"
data = {
    "today": {"value": today2, "color": get_random_color()},
    "week": {"value": getWeek(), "color": get_random_color()},
    "city": {"value": city, "color": get_random_color()},
    "weather": {"value": weather, "color": get_random_color()},
    "min_temperature": {"value": low, "color": "#0f78f6"},
    "max_temperature": {"value": high, "color": "#f94608"},
    "love_days": {"value": get_count(), "color": "#e2101c"},
    "birthday_left": {"value": get_birthday(), "color": "#8131eb"},
    "words": {"value": get_words(), "color": get_random_color()},
}
res = wm.send_template(user_id, template_id, data)
print(res)
