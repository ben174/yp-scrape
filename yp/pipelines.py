# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import sys

import boto
import boto.s3
from boto.s3.key import Key

import settings


class ResultPipeline(object):
    def __init__(self):
        self.results = []

    def process_item(self, item, spider):
        self.results.append(item)
        return item

    def close_spider(self, spider):
        pass


class JsonFilePipeline(object):
    def __init__(self):
        if not os.path.exists(settings.JSON_PATH):
            os.makedirs(settings.JSON_PATH)

    def process_item(self, item, spider):
        filename = item.get_filename(suffix='.json')
        path = os.path.join(settings.JSON_PATH, filename)
        print 'Writing file to path: ' + path
        try:
            os.remove(path)
        except OSError:
            pass
        f = open(path, 'w')
        f.write(item.get_json())
        f.flush()
        f.close()
        return item


class JsonS3Pipeline(object):
    def __init__(self):
        bucket_name = settings.S3_BUCKET
        conn = boto.connect_s3(
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY
        )
        self.bucket = conn.get_bucket(bucket_name)

    def process_item(self, item, spider):
        k = Key(self.bucket)
        k.key = item.get_filename(suffix='.json')
        k.set_contents_from_string(item.get_json())
        return item


class WebSocketPipeline(object):
    """ Thought it might be fun to make results stream to a WebSocket
    as they become available. """
    def __init__(self):
        self.results = []

    def process_item(self, item, spider):
        if spider.socket:
            spider.socket.write_message(item.get_json())
        return item

    def close_spider(self, spider):
        pass
