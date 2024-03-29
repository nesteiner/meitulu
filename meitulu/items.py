# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Image(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    album_name = scrapy.Field()
    from_url = scrapy.Field()

class Album(scrapy.Item):
    name = scrapy.Field()
    images = scrapy.Field()