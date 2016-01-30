# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class ResultPipeline(object):
    def __init__(self):
        self.results = []

    def process_item(self, item, spider):
        self.results.append(item)
        return item

    def close_spider(self, spider):
        print 'The spider is done.'
        for result in self.results:
            print 'Here lies a result:'
            print result
            print


class JsonFilePipeline(object):
    def __init__(self):
        self.results = []

    def process_item(self, item, spider):
        self.results.append(item)
        return item

    def close_spider(self, spider):
        print 'The spider is done.'
        for result in self.results:
            print 'Here lies a result:'
            print result
            print

class JsonS3Pipeline(object):
    def __init__(self):
        self.results = []

    def process_item(self, item, spider):
        self.results.append(item)
        return item

    def close_spider(self, spider):
        print 'The spider is done.'
        for result in self.results:
            print 'Here lies a result:'
            print result
            print

class WebSocketPipeline(object):
    """ Thought it might be fun to make results stream to a WebSocket
    as they become available. """
    def __init__(self):
        self.results = []

    def process_item(self, item, spider):
        if spider.socket:
            spider.socket.write_message(json.dumps(dict(item)))
        return item

    def close_spider(self, spider):
        pass

