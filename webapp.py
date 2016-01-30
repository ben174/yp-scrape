import json
import requests
import tornado.websocket
import tornado.httpserver
from scrapy.crawler import CrawlerProcess
from tornado.web import StaticFileHandler

from yp.spiders.result_crawler import ResultSpider



############################################################
#
# Unfortunately, the CORS restrictions on scrapyd meant
# I had to basically proxy all their API calls
#
############################################################

class ScrapyDLogHandler(tornado.web.RequestHandler):
    def get(self, job):
        lines = requests.get('http://192.168.99.100:32768/items/yp/ypcrawl/{}.jl'.format(job)).text.splitlines()
        ret = []
        for line in lines:
            try:
                ret.append(json.loads(line))
            except:
                # probably a partial line, just ignore it
                pass
        self.write(json.dumps(ret))


class ScrapyDJobHandler(tornado.web.RequestHandler):
    def post(self):
        payload = json.loads(self.request.body)
        response = requests.post('http://192.168.99.100:32768/schedule.json', data=payload)
        self.write(response.text)

    def get(self, job=None):
        response = requests.get('http://192.168.99.100:32768/listjobs.json?project=yp').json()
        states = ['running', 'finished', 'pending']
        ret = {'state': None}
        for state in states:
            if job in [j['id'] for j in response[state]]:
                ret['state'] = state
                self.write(json.dumps(ret))


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


if __name__ == "__main__":
    application = tornado.web.Application([
        (r'/scrape/(.*)/(.*)', ScrapeWebSocket),
        (r'/log/(.*)', ScrapyDLogHandler),
        (r'/job', ScrapyDJobHandler),
        (r'/job/(.*)', ScrapyDJobHandler),
        (r'/(.*)', StaticFileHandler, {'path': 'web/'}),
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
