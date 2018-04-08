# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class ImageItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class pexelsItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field() # 完整URL
    title = scrapy.Field() # 图片描述
    tags = scrapy.Field() # 标签
    image_url = scrapy.Field() # 图片URL
    images_local = scrapy.Field() # 图片本地