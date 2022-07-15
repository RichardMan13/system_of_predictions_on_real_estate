# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = scrapy.Field()
    rooms = scrapy.Field()
    suites = scrapy.Field()
    bathrooms = scrapy.Field()
    garages = scrapy.Field()
    private_area = scrapy.Field()
    total_area = scrapy.Field()


