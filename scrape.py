#!/usr/bin/env python

import tornado.websocket
import tornado.httpserver
import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from yp.spiders.result_crawler import ResultSpider


pipelines = {
    'yp.pipelines.ResultPipeline': 300,
}
process = CrawlerProcess({
    'ITEM_PIPELINES': pipelines,
})
process.crawl(ResultSpider, query='Mexican', location='Fremont, CA')
process.start()


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        pipelines = {
            'yp.pipelines.WebSocketPipeline': 300,
        }
        process = CrawlerProcess({
            'ITEM_PIPELINES': pipelines,
        })
        process.crawl(ResultSpider)
        process.start()
        import pdb
        pdb.set_trace()
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")



#application = tornado.web.Application([
#    (r'/ws', EchoWebSocket),
#])

if __name__ == "__main__":
    pass

    # http_server = tornado.httpserver.HTTPServer(application)
    # http_server.listen(8888)
    # tornado.ioloop.IOLoop.instance().start()

