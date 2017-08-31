# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
import os
try:
    from PIL import Image
except:
    pass



class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    header = {
        "Host":"www.zhihu.com",
        "Referer": "https://www.zhizhu.com ",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "X-Xsrftoken": "94b00dab251cccb7ae9b858258a6800c",
    }

    def parse(self, response):
        pass

    def start_requests(self):
        t = str(int(time.time() * 1000))
        captcha_url = "https://www.zhihu.com/captcha.gif?r=" + t + "&type=login&lang=cn"
        return [scrapy.Request(captcha_url, headers=self.header, callback=self.parser_captcha)]

    def parser_captcha(self, response):
        with open('captcha.jpg', 'wb') as f:
            f.write(response.body)
            f.close()
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
        captcha = input("please input the captcha\n>")
        return [scrapy.Request('https://www.zhihu.com/', headers=self.header, callback=self.login, meta={'captcha':captcha}, dont_filter=True)]


    def login(self, response):
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text, re.DOTALL)
        print(response.meta['captcha'])
        xsrf = ''
        if match_obj:
            xsrf = match_obj.groups(1)
        if xsrf:
            post_data = {
                "_xsrf": xsrf,
                "captcha_type": "cn",
                "phone_num": "18700000000",
                "password": "password",
                "captcha_type": "cn",
                'captcha': response.meta['captcha'],
            }

        post_url = "https://www.zhihu.com/login/phone_num"

        return [scrapy.FormRequest(
            method='POST',
            url = post_url,
            headers = self.header,
            callback = self.check_login,
            dont_filter=True,
            # check_login不带后面括号，传递函数对象
        )]


    def check_login(self, response):
        # 验证是否登入成功
        json_file = json.loads(response.text)
        print(json_file)
        if json_file['r'] == 0:
            print('success........登录成功')
        else:
            print('登录失败！')

        if "msg" in json_file and json_file["msg"] == "登入成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.header)
        pass
