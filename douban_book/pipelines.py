# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
import json
import codecs

# 连接数据库,类名要跟settings里面设置的名字一致
class MySQLStorePipeline(object):

    # 数据库配置
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('pymysql',
                                            db='crawler',
                                            user='root',
                                            passwd='123456',
                                            cursorclass=pymysql.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=False
                                            )

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    # 将每行写入数据库中
    def _conditional_insert(self, tx, item):
        tx.execute('INSERT INTO douban_book (bookName, bookRate, bookDes, bookUrl) VALUES (%s, %s, %s, %s);',
                   (item['bookName'], item['bookRate'], item['bookDes'], item['bookUrl']))
