# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    detail_title = scrapy.Field()
    detail_title_url = scrapy.Field()
    book_name = scrapy.Field()
    book_image = scrapy.Field()
    book_info = scrapy.Field()
    book_author = scrapy.Field()
    book_url = scrapy.Field()
    book_price = scrapy.Field()
