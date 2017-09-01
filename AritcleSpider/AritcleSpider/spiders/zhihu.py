# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
import os
import datetime
from scrapy.loader import ItemLoader
from AritcleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem
try:
    from PIL import Image
except:
    pass

try:
    import urlparse as parse
except:
    from urllib import parse



class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    header = {
        "Host":"www.zhihu.com",
        "Referer": "https://www.zhizhu.com ",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "X-Xsrftoken": "94b00dab251cccb7ae9b858258a6800c",
    }

    def parse(self, response):
        # 提取出页面中的所以url，并跟踪这些url进行下一步爬取
        # 如果提取的url格式为/question/xx 就下载知乎直接进入解析函数
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x:True if x.startwith("https") else False, all_urls)
        for url in  all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url, re.DOTALL)
            if match_obj:
                # 如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.groups(1)
                yield scrapy.Request(request_url, headers=self.header, callback=self.parse_question)
            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.header, callback=self.parse)

    def parse_question(self, response):
        # 处理question页面，从页面提取出具体的question item

        if "QuestionHeader-title" in response.text:
            # 处理新版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url, re.DOTALL)
            if match_obj:
                question_id = int(match_obj.groups(2))
            item_load = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_load.add_css("title", "h1.QuestionHeader-title::text")
            item_load.add_css("content", "QuestionHeader-detail")
            item_load.add_value("url", response.url)
            item_load.add_value("zhihu_id", question_id)
            item_load.add_css("answer_num", ".List-headerText span:text")
            item_load.add_css("comments_num", "QuestionHeader-actions button:text")
            item_load.add_css("watch_user_num", "NumberBoard-value::text")
            item_load.add_css("topics", "QuestionHeader-topics .Popover::text")

            question_itm = item_load.load_item()

        else:
            # 处理老版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            # item_loader.add_css("title", ".zh-question-title h2 a::text")
            item_loader.add_xpath("title",
                                  "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            # item_loader.add_css("watch_user_num", "#zh-question-side-header-wrap::text")
            item_loader.add_xpath("watch_user_num",
                                  "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()

            yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), callback=self.parse_answer)
            yield question_item


    def parse_answer(self, reponse):
        # 处理question的answer
        ans_json = json.loads(reponse.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)




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
