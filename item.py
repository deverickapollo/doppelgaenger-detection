import scrapy

class guardianbotItem(scrapy.Item):
    title = scrapy.Field(default="null")
    author = scrapy.Field(default="null")
    url = scrapy.Field(default="null")
    publish_date = scrapy.Field(default="null")
    publish_time = scrapy.Field(default="null")