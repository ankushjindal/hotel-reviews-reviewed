# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkItem(scrapy.Item):
	title = scrapy.Field()
	tripadvisorU = scrapy.Field()
	tripadvisorR = scrapy.Field()
	holidayiqU = scrapy.Field()
	holidayiqR = scrapy.Field()
	location = scrapy.Field()
	price = scrapy.Field()
	stars= scrapy.Field()
	amenities = scrapy.Field()