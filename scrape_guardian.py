#!/usr/bin/python
# Helper functions to crawl Guardian News Website
import logging, re, pytz, requests, scrapy
from scrapy import *
from datetime import datetime, timezone as ttime
import pytz
from pytz import timezone

bst = pytz.timezone('Europe/London')
TAG_RE = re.compile(r'<[^>]+>')
aedt = pytz.timezone('Australia/Tasmania')

class guardianSpider(scrapy.Spider):
    name = "toscrape-css"

    def __init__(self, *args, **kwargs):
        super(guardianSpider, self).__init__(*args, **kwargs)
        conn = kwargs.get('connection')
        if not conn:
            raise ValueError('No connection argument available')
        self.start_urls = ['https://www.theguardian.com/international']

    def parse(self, response):
        for url in response.css("h3.fc-item__title"):
            link = url.css("a::attr(href)").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'url': link})
        for url in response.css("h4.fc-sublink__title"):
            link = url.css("a::attr(href)").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'url': link})

    def parse_article(self, response):
        date = response.xpath('//*[@class="css-1kkxezg"]//text()').extract_first()
        title = response.xpath('normalize-space(//h1//text())').get()
        author = response.xpath('//*[@rel="author"]//text()').extract_first()
        comments = response.css("#comments").get()
        if comments:
            # fetch discussion via shortUrlId from guardian discussion API
            shortUrlId = response.xpath("//script[contains(text(), 'shortUrlId')]//text()").get()
            shortUrlId = shortUrlId.partition('shortUrlId":"')[2][:8]
            discussion = requests.get(
                'http://discussion.theguardian.com/discussion-api/discussion/' + shortUrlId).json()
            comment_count = discussion['discussion']['commentCount']
        else:
            comment_count = 0
        if not date:
            date = response.css("time.content__dateline-wpd::text").extract_first() + response.css(
                "span.content__dateline-time::text").extract_first()
        if not title:
            title = response.css('h1 span::text').get()
        if not author:
            author = ''.join(response.xpath('//*[@class="css-1rv9jci"]//text()').extract())
        date_stripped = date.replace("\n", "")
        date_stripped = date_stripped.strip()
        date_xa0 = date_stripped.replace(u'\xa0', u' ')
        #HANDLE TIMESTAMPS. Find better logic here. Moving back to date for now until values are needed. Could also leave logic during frontend processing.
        # if (date_xa0.find('BST') != -1):
        #     scrubbed = date_xa0[:-4]
        #     naive = datetime.strptime(scrubbed, "%a %d %b %Y %H.%M")
        #     local_dt = bst.localize(naive, is_dst=None)
        #     timestamp = local_dt.astimezone(pytz.utc).timestamp()
        # elif (date_xa0.find('AEDT') != -1):
        #     scrubbed = date_xa0[:-4]
        #     naive = datetime.strptime(scrubbed, "%a %d %b %Y %H.%M")
        #     local_dt = aedt.localize(naive, is_dst=None)
        #     timestamp = local_dt.astimezone(pytz.utc).timestamp()
        # else:
        #     time_in_datetime = datetime.strptime(date_xa0, "%a %d %b %Y %H.%M %Z")
        #     timestamp = time_in_datetime.replace(tzinfo=ttime.utc).timestamp()
        yield {
            'title': title, #string
            'url': response.meta.get('url'), #string
            'author': author, #string
            'publish_date': date, #datetime object stored as a timestamp from epoch
            'comment_count': comment_count #int
        }

class commentSpider(scrapy.Spider):
    name = "toscrape-comment-css"

    def __init__(self, *args, **kwargs):
        super(commentSpider, self).__init__(*args, **kwargs)
        conn = kwargs.get('connection')
        if not conn:
            raise ValueError('No connection argument available')
        self.start_urls = ['https://www.theguardian.com/international']

    def parse(self, response):
        for url in response.css("h3.fc-item__title"):
            link = url.css("a::attr(href)").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'url': link})
        for url in response.css("h4.fc-sublink__title"):
            link = url.css("a::attr(href)").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'url': link})

    def parse_article(self, response):
        comments = response.css("#comments").get()
        if comments:
            # fetch discussion via shortUrlId from guardian discussion API
            shortUrlId = response.xpath("//script[contains(text(), 'shortUrlId')]//text()").get()
            shortUrlId = shortUrlId.partition('shortUrlId":"')[2][:8]
            discussion = requests.get('http://discussion.theguardian.com/discussion-api/discussion/' + shortUrlId).json()

            for page_number in range(1, discussion['pages']+1):
                discussion = requests.get(
                    'http://discussion.theguardian.com/discussion-api/discussion/' + shortUrlId + '?page=' + str(page_number)).json()
                for comment in discussion['discussion']['comments']:
                    if 'responses' in comment:
                        for comment_response in comment['responses']:
                            yield {
                                'comment_id': comment_response['id'],
                                'comment_text': TAG_RE.sub('', comment_response['body']),
                                'comment_date': comment_response['isoDateTime'],
                                'comment_author_id': comment_response['userProfile']['userId'],
                                'comment_author_username': comment_response['userProfile']['displayName'],
                                'article_url': response.meta.get('url'),
                                'article_title': discussion['discussion']['title']
                            }
                    else:
                        yield {
                                'comment_id': comment['id'],
                                'comment_text': TAG_RE.sub('', comment['body']),
                                'comment_date': comment['isoDateTime'],
                                'comment_author_id': comment['userProfile']['userId'],
                                'comment_author_username': comment['userProfile']['displayName'],
                                'article_url': response.meta.get('url'),
                                'article_title': discussion['discussion']['title']
                            }




