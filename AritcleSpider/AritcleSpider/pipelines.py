# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
# codecs为python的开发包，可避免编码方面的问题
import json
import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
# adbapi:此模块把mysql变成异步化操作



class AritclespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # ensure_ascii=False:为了防止输入中文时候出现错误，非常重要
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

class JsonExporterPipeline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open("articleexport.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    # 采用同步的mysql
    def __init__(self):
        self.conn = MySQLdb.connect('10.163.46.92', 'root', 'qwe123', 'article_spider',
                                    charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, create_date, url, fav_nums, url_object_id)
            VALUE (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["fav_nums"], item["url_object_id"]))
        self.conn.commit()
        return item

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        此方法会被spider调用，然后调用这个项目的settings文件，方法名称是固定的。
        """
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWD"],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变为异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error) # 处理异常


    def handle_error(self, failure, items, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                    insert into jobbole_article(title, create_date, url, fav_nums, url_object_id)
                    VALUE (%s, %s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["fav_nums"], item["url_object_id"]))




class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path

        return item


