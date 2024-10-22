# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class XPostItem(scrapy.Item):
    tweetText = scrapy.Field()
    User_Name = scrapy.Field()
    isPost = scrapy.Field()
    get_timestamp = scrapy.Field()
    stats = scrapy.Field()
    # tweetPhoto = scrapy.Field()
