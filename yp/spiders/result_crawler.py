import urllib

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from yp.items import ResultItem



class ResultSpider(CrawlSpider):
    name = 'ypcrawl'
    allowed_domains = ['yellowpages.com']

    rules = (
        Rule(LinkExtractor(restrict_css='.next.ajax-page'),
            callback='parse_page', follow=True
        ),
    )

    def __init__(self, query='Cupcakes', location='Tucson, AZ', socket=None, *args, **kwargs):
        self.query = query
        self.location = location
        self.start_urls = [self._get_url(query, location)]
        self.socket = socket
        super(ResultSpider, self).__init__(*args, **kwargs)

    def _get_url(self, query, location, page=None):
        """ Constructs a result page URL """
        params = { 'search_terms' : query, 'geo_location_terms' : location }
        if page:
            params['page'] = page
        query = urllib.urlencode(params)
        return 'http://www.yellowpages.com/search?{}'.format(query)

    def parse_start_url(self, response):
        """
        Ensures the first page is scraped, as well as crawled for next links.
        """
        return self.parse_page(response)

    def parse_page(self, response):
        """
        Scrapes a result page, yielding ResultItems from .srp-listing elements.
        """
        selector = scrapy.Selector(response)
        results = selector.css(".srp-listing")

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
            yield item
