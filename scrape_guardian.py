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
    custom_settings = {'ITEM_PIPELINES': {'db_pipeline.sqLitePipeline': 300}}

    # pipeline = set([
    #     db_pipeline.sqLitePipeline,
    # ])
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
        # HANDLE TIMESTAMPS. Find better logic here. Moving back to date for now until values are needed. Could also leave logic during frontend processing.
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
            'title': title,  # string
            'url': response.meta.get('url'),  # string
            'author': author,  # string
            'publish_date': date,  # datetime object stored as a timestamp from epoch
            'comment_count': comment_count  # int
        }


class commentSpider(scrapy.Spider):
    name = "toscrape-comment-css"

    # pipeline = set([
    #     db_pipeline.commentPipeline,
    # ])
    custom_settings = {'ITEM_PIPELINES': {'db_pipeline.commentPipeline': 300}}

    def __init__(self, *args, **kwargs):
        super(commentSpider, self).__init__(*args, **kwargs)
        conn = kwargs.get('connection')
        if not conn:
            raise ValueError('No connection argument available')
        self.start_urls = ['https://www.theguardian.com/international']

    def parse(self, response):
        # walk through the links on the index page and yield new requests
        for url in response.css("h3.fc-item__title"):
            link = url.css("a::attr(href)").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'url': link})
        for url in response.css("h4.fc-sublink__title"):
            link = url.css("a::attr(href)").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'url': link})

        # read user ids from file
        ids = []
        with open('misc/ids.txt', 'r') as filehandle:
            for line in filehandle:
                # remove linebreak which is the last character of the string
                currentPlace = line[:-1]
                # add item to the list
                if currentPlace not in ids:
                    ids.append(currentPlace)

        # for every user id call the guardian discussion api and fetch the latest 200 comments
        for id in ids:
            user_comments = requests.get('http://discussion.theguardian.com/discussion-api/profile/' + str(
                id) + '/comments?pageSize=100&page=1').json()
            for user_comment in user_comments['comments']:
                yield {
                    'comment_id': user_comment['id'],
                    'comment_text': TAG_RE.sub('', user_comment['body']),
                    'comment_date': user_comment['isoDateTime'],
                    'comment_author_id': user_comments['userProfile']['userId'],
                    'comment_author_username': user_comments['userProfile']['displayName'],
                    'article_url': user_comment['discussion']['webUrl'],
                    'article_title': user_comment['discussion']['title']
                }
            if user_comments['pages'] > 1:
                user_comments = requests.get('http://discussion.theguardian.com/discussion-api/profile/' + str(
                    id) + '/comments?pageSize=100&page=2').json()
                for user_comment in user_comments['comments']:
                    yield {
                        'comment_id': user_comment['id'],
                        'comment_text': TAG_RE.sub('', user_comment['body']),
                        'comment_date': user_comment['isoDateTime'],
                        'comment_author_id': user_comments['userProfile']['userId'],
                        'comment_author_username': user_comments['userProfile']['displayName'],
                        'article_url': user_comment['discussion']['webUrl'],
                        'article_title': user_comment['discussion']['title']
                    }

        # delete duplicate ids from file
        with open('misc/ids.txt', 'r') as f:
            unique_lines = set(f.readlines())
        with open('misc/ids.txt', 'w') as f:
            f.writelines(unique_lines)

    def parse_article(self, response):
        # fetch discussion via shortUrlId from guardian discussion API
        comments = response.css("#comments").get()
        if comments:
            user_ids = []
            shortUrlId = response.xpath("//script[contains(text(), 'shortUrlId')]//text()").get()
            shortUrlId = shortUrlId.partition('shortUrlId":"')[2][:8]
            discussion = requests.get(
                'http://discussion.theguardian.com/discussion-api/discussion/' + shortUrlId).json()
            for page_number in range(1, discussion['pages'] + 1):
                discussion = requests.get(
                    'http://discussion.theguardian.com/discussion-api/discussion/' + shortUrlId + '?page=' + str(
                        page_number)).json()

                # for each comment fetch user id
                for comment in discussion['discussion']['comments']:
                    if 'responses' in comment:
                        for comment_response in comment['responses']:
                            if user_ids.append(comment_response['userProfile']['userId']) not in user_ids:
                                user_ids.append(comment_response['userProfile']['userId'])
                    else:
                        if user_ids.append(comment['userProfile']['userId']) not in user_ids:
                            user_ids.append(comment['userProfile']['userId'])

            # save user ids in file
            for user_id in user_ids:
                with open("misc/ids.txt", "a") as myfile:
                    myfile.write(user_id + "\n")
