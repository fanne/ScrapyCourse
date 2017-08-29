# -*- coding:utf-8 -*-


import requests
import re
import time
import os
try:
    import cookielib
    # python 2中叫做cookielib，使用try except这种写法可以兼容python2
except:
    import http.cookiejar as cookielib
try:
    from PIL import Image
except:
    pass


"""
知乎倒立验证码
https://github.com/xchaoinfo/fuck-login/blob/master/001%20zhihu/zhihu.py
http://blog.5ibc.net/p/147532.html
获得了倒立汉字图片以后，如何确定要传递给知乎的captcha是什么呢？经过Fiddler抓包，
传递的参数类似于这样：
{"img_size":[200,44],"input_points":[[43.44,22.44],[115.72,22.44]]}
经过分析和试验确定：200指的是图片长度，44指的是图片高度，后面的input_points指的是打在倒立汉字上的点的坐标。由于每次出现7个汉字，这7个汉字的坐标是固定的，我全部进行捕获：
{"img_size":[200,44],"input_points":[[12.95,14.969999999999998],[36.1,16.009999999999998],[57.16,24.44],[84.52,19.17],[108.72,28.64],[132.95,24.44],[151.89,23.380000000000002]]}
然后，问题就简单了：将图片保存在本地之后，打开图片，确定哪几个汉字倒立，比如说第2个和第6个，那就在上面选取出2和6的坐标输入即可，即
{"img_size":[200,44],"input_points":[[36.1,16.009999999999998],[132.95,24.44]]}。
"""


session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")


try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookies 未能加载")


agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"
header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Host":"www.zhihu.com",
    "Referer": "https://www.zhizhu.com ",
    'User-Agent': agent,
}


def is_login():
    # 通过个人中心判断是否已登入
    index_url = "https://www.zhihu.com/inbox"
    response = session.get(index_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=header)
    # requests.get在请求的时候，设置的header为python2,python3的，而非浏览器的header
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
    # 一个元字符是 . 它匹配除了换行字符外的任何字符，在 alternate 模式（re.DOTALL）下它甚至可以匹配换行。"." 通常被用于你想匹配“任何字符”的地方。
    # (DOTALL): 点任意匹配模式，改变'.'的行为
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r=" + t + "&type=login&lang=cn"
    r = session.get(captcha_url, headers=header)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha




def zhihu_login(account, pawword):
    # 知乎登入
    if re.match("^1\d{10}",account):
        print("手机号码登入")
        post_url = "https://www.zhihu.com/login/phone_num"
        print(get_xsrf(),account,pawword)
        post_data = {
            "_xsrf": get_xsrf(),
            "captcha_type": "cn",
            "phone_num": account,
            "password": pawword
        }
    else:
        if "@" in account:
            print("邮箱登入")
            post_url = "https://www.zhihu.com/login/email"
            print(get_xsrf(), account, pawword)
            post_data = {
                "_xsrf": get_xsrf(),
                "captcha_type": "cn",
                "email": account,
                "password": pawword
            }
    response_text = session.post(post_url, data=post_data, headers=header)
    print(response_text.status_code)
    if response_text.status_code == 200:
        if response_text.json()["r"] == 1:
            post_data["captcha"] = get_captcha()
            response_text = session.post(post_url, data=post_data, headers=header)
            print(response_text.status_code)
            print(response_text.json())
    session.cookies.save()



if __name__ == '__main__':
    zhihu_login("18700000000", "password")
    # get_index()
    # is_login()
