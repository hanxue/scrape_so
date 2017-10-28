# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from scrapy.exceptions import DropItem
from so_jobs.items import ModelItem

db = SqliteExtDatabase('stackoverflow.db', journal_mode='WAL')

class SQLitePipeline(object):
    def __init__(self):
        db.connect()
        if not StackJob.table_exists():
            StackJob.create_table()

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            job = StackJob(**item)
            job.save()
            # self.cursor.execute(
            #     "INSERT INTO stackjobmodel (company, title, location, perks, url)" +
            #     " values (?, ?, ?, ?, ?)",
            #         (item['company'], item['title'], item['location'], item['perks'], item['url'])
            # )

        return item

class BaseModel(Model):
    class Meta:
        database = db

class StackJob(BaseModel):
    company = CharField()
    title = CharField()
    location = CharField()
    perks = CharField()
    url = CharField()