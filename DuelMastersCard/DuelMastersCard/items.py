# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DuelmasterscardItem(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field()
    civilization = scrapy.Field()
    tribe = scrapy.Field()
    cost = scrapy.Field()
    power = scrapy.Field()
    effect = scrapy.Field()
    collections = scrapy.Field()
