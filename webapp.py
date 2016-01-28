import tornado.websocket
import tornado.httpserver
from scrapy.crawler import CrawlerProcess
from tornado.web import StaticFileHandler

from yp.spiders.result_crawler import ResultSpider



class ScrapeWebSocket(tornado.websocket.WebSocketHandler):
    def open(self, query, location):
        pipelines = {
            'yp.pipelines.WebSocketPipeline': 300,
        }
        process = CrawlerProcess({
            'ITEM_PIPELINES': pipelines,
        })
        process.crawl(ResultSpider, query=query, location=location, socket=self)
        process.start()
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r'/scrape/(.*)/(.*)', ScrapeWebSocket),
        (r'/(.*)', StaticFileHandler, {'path': 'web/'}),
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
