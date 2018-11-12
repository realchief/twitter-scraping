# -*- coding: utf-8 -*-
import os
import re
import json
import datetime
import scrapy
import math
import pandas as pd

from scrapy import Request
from lxml import html
from urlparse import urljoin
from items import TwitterItem


class SwedishTwitterSpider(scrapy.Spider):
    name = 'swedish_twitter'

    allowed_domains = ["twitter.com"]

    start_urls = ['https://twitter.com/search-home']

    search_url = 'https://twitter.com/search?q={keyword}&src=typd'

    next_page_url = 'https://twitter.com/i/search/timeline?vertical=default&q={keyword}&src=typd&' \
                    'include_available_features=1&include_entities=1&max_position={max_position}&reset_error_state=false'

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    def __init__(self, *args, **kwargs):
        super(SwedishTwitterSpider, self).__init__(site_name=self.allowed_domains[0], *args, **kwargs)
        self.current_page = 0

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        excel_path = os.path.dirname(os.path.abspath(__file__)).replace('twitter_scraping/spiders',
                                                                        'KeyWords for Depression.xlsx')
        df = pd.read_excel(excel_path)
        keywords = []

        swedish_keyword = df['Swedish ']
        for keyword in swedish_keyword:
            nan_value = False
            try:
                if math.isnan(keyword):
                    nan_value = True
            except:
                pass
            if not nan_value:
                keywords.append(keyword.encode('utf-8'))

        for keyword in keywords:
            search_url = self.search_url.format(keyword=self._clean_text(keyword))
            meta = response.meta
            meta['keyword'] = self._clean_text(keyword)
            yield Request(
                url=search_url,
                callback=self.parse_twitter_page,
                headers=self.headers,
                meta=meta
            )

    def parse_twitter_page(self, response):
        meta = response.meta
        keyword = meta.get('keyword')

        data = None
        json_data = None
        html_data = None
        try:
            data = json.loads(response.body)
            json_data = True
        except:
            pass
        if not data:
            data = response.body
            html_data = True

        if html_data:
            posts = response.xpath('//li[@data-item-type="tweet"]').extract()
            min_position = re.search('data-min-position="(.*?)"', data)
            if min_position:
                min_position = min_position.group(1)
            next_page = self.next_page_url.format \
                (keyword=keyword,
                 max_position=min_position.replace('cm+', 'cm%2B').replace('==', '%3D%3D')
                 )

            for post in posts:
                time_stamp = int(html.fromstring(post).xpath('//small[@class="time"]/a/span/@data-time')[0])
                twitter_time = datetime.datetime.fromtimestamp(time_stamp).strftime("%Y-%m-%d %H:%M:%S")
                post_year = int(datetime.datetime.fromtimestamp(time_stamp).strftime("%Y"))
                current_year = datetime.datetime.now().year
                if post_year < int(current_year) - 2:
                    next_page = None
                    break
                author = self._clean_text(
                    html.fromstring(post).xpath('//span[@class="FullNameGroup"]/strong/text()')[0])
                content = self._clean_text(' '.join(html.fromstring(post)
                                                    .xpath('//p[contains(@class, "TweetTextSize")]/text()'))).encode(
                    'utf-8')

                replies_count = html.fromstring(post) \
                    .xpath('//div[contains(@class, "ProfileTweet-action--reply")]//'
                           'span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(replies_count) > 0:
                    replies_count = int(replies_count[0])
                else:
                    replies_count = 0

                retweet_count = html.fromstring(post) \
                    .xpath('//div[contains(@class, "ProfileTweet-action--retweet")]//'
                           'span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(retweet_count) > 0:
                    retweet_count = int(retweet_count[0])
                else:
                    retweet_count = 0

                like_count = html.fromstring(post) \
                    .xpath('//div[contains(@class, "ProfileTweet-action--favorite")]//'
                           'span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(like_count) > 0:
                    like_count = int(like_count[0])
                else:
                    like_count = 0

                twitter = TwitterItem()
                twitter['Author'] = author
                twitter['Content'] = content
                twitter['TwitterTime'] = twitter_time
                twitter['RepliesCount'] = replies_count
                twitter['RetweetCount'] = retweet_count
                twitter['LikeCount'] = like_count

                meta = response.meta
                meta['twitter'] = twitter

                author_link = urljoin(response.url, html.fromstring(post)
                                      .xpath('//div[@class="stream-item-header"]/a/@href')[0])
                if author_link:
                    yield Request(
                        url=author_link,
                        callback=self.parse_author,
                        meta=meta,
                        headers=self.headers,
                        dont_filter=True)

        elif json_data:
            json_data = json.loads(response.body)
            min_position = json_data.get('min_position')
            posts = html.fromstring(json_data.get('items_html')).xpath('//li[@data-item-type="tweet"]')
            next_page = self.next_page_url.format \
                (keyword=keyword,
                 max_position=min_position.replace('cm+', 'cm%2B').replace('==', '%3D%3D')
                 )

            for post in posts:
                str_data = html.tostring(post)
                time_stamp = int(html.fromstring(str_data).xpath('//small[@class="time"]/a/span/@data-time')[0])
                twitter_time = datetime.datetime.fromtimestamp(time_stamp).strftime("%Y-%m-%d %H:%M:%S")
                post_year = int(datetime.datetime.fromtimestamp(time_stamp).strftime("%Y"))
                current_year = datetime.datetime.now().year
                if post_year < int(current_year) - 2:
                    next_page = None
                    break
                author = self._clean_text(
                    html.fromstring(str_data).xpath('//span[@class="FullNameGroup"]/strong/text()')[0])
                content = self._clean_text(
                    ' '.join(html.fromstring(str_data).xpath('//p[contains(@class, "TweetTextSize")]/text()'))).encode(
                    'utf-8')

                replies_count = html.fromstring(str_data).xpath(
                    '//div[contains(@class, "ProfileTweet-action--reply")]//'
                    'span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(replies_count) > 0:
                    replies_count = int(replies_count[0])
                else:
                    replies_count = 0

                retweet_count = html.fromstring(str_data).xpath(
                    '//div[contains(@class, "ProfileTweet-action--retweet")]//'
                    'span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(retweet_count) > 0:
                    retweet_count = int(retweet_count[0])
                else:
                    retweet_count = 0

                like_count = html.fromstring(str_data).xpath(
                    '//div[contains(@class, "ProfileTweet-action--favorite")]//'
                    'span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(like_count) > 0:
                    like_count = int(like_count[0])
                else:
                    like_count = 0

                twitter = TwitterItem()
                twitter['Author'] = author
                twitter['Content'] = content
                twitter['TwitterTime'] = twitter_time
                twitter['RepliesCount'] = replies_count
                twitter['RetweetCount'] = retweet_count
                twitter['LikeCount'] = like_count

                meta = response.meta
                meta['twitter'] = twitter

                author_link = urljoin(response.url,
                                      html.fromstring(str_data).xpath('//div[@class="stream-item-header"]/a/@href')[0])
                if author_link:
                    yield Request(
                        url=author_link,
                        callback=self.parse_author,
                        meta=meta,
                        headers=self.headers,
                        dont_filter=True)

        if next_page:
            yield scrapy.http.Request(
                url=next_page,
                callback=self.parse_twitter_page,
                headers=self.headers,
                meta=meta
            )
        else:
            return

    def parse_author(self, response):
        meta = response.meta
        twitter = meta['twitter']
        username = response.xpath('//a[contains(@class, "ProfileHeaderCard-screennameLink")]/'
                                  'span[contains(@class, "username")]/b/text()').extract()[0].encode('utf-8')
        tweet_count = int(response.xpath('//li[contains(@class, "ProfileNav-item--tweets is-active")]//'
                                         'span[@class="ProfileNav-value"]/@data-count').extract()[0])
        follower_count = int(response.xpath('//li[contains(@class, "ProfileNav-item--followers")]//'
                                            'span[@class="ProfileNav-value"]/@data-count').extract()[0])
        author_location = self._clean_text(response.xpath('//span[contains(@class, "ProfileHeaderCard-locationText")]/'
                                                          'text()').extract()[0])

        twitter['Username'] = username
        twitter['TweetCount'] = tweet_count
        twitter['FollowerCount'] = follower_count
        twitter['AuthorLocation'] = author_location

        return twitter

    @staticmethod
    def _clean_text(text):
        text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
        text = re.sub("&nbsp;", " ", text).strip()

        return re.sub(r'\s+', ' ', text)