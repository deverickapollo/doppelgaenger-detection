import scrapy

class guardianbotItem(scrapy.Item):
    title = scrapy.Field(default="null")
    author = scrapy.Field(default="null")
    url = scrapy.Field(default="null")
    publish_date = scrapy.Field(default="null")
    comment_count = scrapy.Field(default="null")

class commentItem():
    comment_id = scrapy.Field(default="null")
    comment_text = scrapy.Field(default="null")
    comment_date = scrapy.Field(default="null")
    comment_author_id = scrapy.Field(default="null")
    comment_author_username = scrapy.Field(default="null")
    article_url = scrapy.Field(default="null")
    article_title = scrapy.Field(default="null")
