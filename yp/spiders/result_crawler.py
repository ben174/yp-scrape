import urllib
import re
import json

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
            item['business_id'] = None

            # some useful json data in here
            data_model = result.css('div.mybook-actions').xpath('@data-model').extract_first()
            if data_model:
                data_model = json.loads(data_model)
                if 'ypid' in data_model:
                    item['business_id'] = data_model['ypid']
            item['is_sponsored'] = 'paid-listing' in result.xpath('@class').extract_first()

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
            item['telephones'] = result.css('.phones').xpath('text()').extract()
            item['categories'] = result.css('.categories > a').xpath('text()').extract()
            item['snippet'] = result.css('.snippet > p').xpath('text()').extract_first()
            item['website'] = result.css('.links').xpath('a[text()="Website"]/@href').extract_first()

            rating_class = result.css('.result-rating').xpath('@class').extract_first()
            nums = {
                'one': 1,
                'two': 2,
                'three': 3,
                'four': 4,
                'five': 5,
            }

            # this feels particularly delicate and heavy, i'd probably move
            # into a result parser module or something
            if rating_class:
                rating_class = rating_class.split(' ')
                for class_name in rating_class:
                    if class_name in nums.keys():
                        item['rating'] = nums[class_name]
                if 'half' in rating_class:
                    item['rating'] += 0.5

            rating_count_str = result.css('.result-rating .count').xpath('text()').extract_first()
            if rating_count_str:
                try:
                    rating_count_str = re.findall(r'\d+', rating_count_str)[0]
                    item['rating_count'] = int(rating_count_str)
                except ValueError as e:
                    print 'Error converting rating value to int: {}'.format(rating_count_str)

            result_num = result.css('h3').xpath('text()').extract_first()
            if result_num:
                try:
                    result_num = re.findall(r'\d+', result_num)[0]
                    item['result_num'] = int(result_num)
                except ValueError as e:
                    print 'Error converting rating value to int: {}'.format(rating_str)

            item['thumbnail_url'] = result.css('.media-thumbnail img').xpath('@data-original').extract_first()
            if item['thumbnail_url']:
                item['thumbnail_url'] = item['thumbnail_url'].strip()

            yield item
