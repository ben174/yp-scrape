import urllib

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from yp.items import ResultItem



class ResultSpider(scrapy.Spider):
    name = 'yp'
    allowed_domains = ['yellowpages.com']

    def __init__(self, query='Cupcakes', location='Tucson, AZ', *args, **kwargs):
        self.current_page = 1
        self.query = query
        self.location = location
        super(ResultSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        while True:
            url = self._get_url(self.query, self.location, page=self.current_page)
            yield scrapy.Request(url, self.parse)
            self.current_page += 1


    def _get_url(self, query, location, page=None):
        params = { 'search_terms' : query, 'geo_location_terms' : location }
        if page:
            params['page'] = page
        query = urllib.urlencode(params)
        return 'http://www.yellowpages.com/search?{}'.format(query)

    def parse(self, response):
        selector = scrapy.Selector(response)
        results = selector.css(".srp-listing")
        items = []

        for result in results:
            item = ResultItem()
            item['business_name'] = result.css('.business-name').xpath('text()').extract_first()
            #item['rating'] = ''
            address_selector = result.css('.adr')
            address_info = address_selector.xpath('span/text()').extract()
            if address_info:
                try:
                    item['street_address'] = address_info[0]
                    item['city'] = address_info[1]
                    item['state'] = address_info[2]
                    item['zip_code'] = address_info[3]
                except IndexError as e:
                    print 'Index error in address info'
            item['telephone'] = result.css('.phones').xpath('text()').extract()
            item['categories'] = result.css('.categories > a').xpath('text()').extract()
            #item['links'] = scrapy.Field()
            #item['location_count'] = scrapy.Field()
            #item['snippet'] = scrapy.Field()
            #item['result_num'] = scrapy.Field()
            items.append(item)
        return items

