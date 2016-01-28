# -*- coding: utf-8 -*-

# Yellow Pages listing item
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ResultItem(scrapy.Item):
    business_id = scrapy.Field()
    business_name = scrapy.Field()
    rating = scrapy.Field()
    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    telephone = scrapy.Field()
    categories = scrapy.Field()
    links = scrapy.Field()
    location_count = scrapy.Field()
    snippet = scrapy.Field()
    result_num = scrapy.Field()
