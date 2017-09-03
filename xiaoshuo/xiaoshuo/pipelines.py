# -*- coding: utf-8 -*-
import sqlite3
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class XiaoshuoPipeline(object):
    def open_spider(self, spider):
        self.conn = sqlite3.connect('xiaoshuo/xiaoshuo.db')

    def process_item(self, item, spider):
        self.conn.execute('INSERT INTO tbl_xiaoshou VALUES(?,?,?,?,?,?);',
        (None, item['name'], item['id'], item['current_url'], int(item['current_page']), item['discussion']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
