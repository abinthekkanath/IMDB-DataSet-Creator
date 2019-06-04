# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbdatasetItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    certification=scrapy.Field()
    duration=scrapy.Field()
    genres=scrapy.Field()
    releaseDate=scrapy.Field()
    summary=scrapy.Field()
    stars=scrapy.Field()
    primaryLanguage=scrapy.Field()
   