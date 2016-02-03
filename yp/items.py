import unicodedata
import re
import json

import scrapy


class ResultItem(scrapy.Item):
    business_id = scrapy.Field()
    business_name = scrapy.Field()
    is_sponsored = scrapy.Field()
    rating = scrapy.Field()
    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    telephones = scrapy.Field()
    categories = scrapy.Field()
    location_count = scrapy.Field()
    snippet = scrapy.Field()
    result_num = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()
    website = scrapy.Field()
    thumbnail_url = scrapy.Field()

    def get_filename(self, suffix=None):
        # borrowed from Django's 'slugify' method
        value = unicodedata.normalize('NFKD', self['business_name']).encode('ascii', 'ignore')
        value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
        value = re.sub('[-\s]+', '-', value)
        if self['business_id']:
            value = self['business_id'] + '-' + value
        return value + suffix

    def get_json(self):
        return json.dumps(dict(self))
