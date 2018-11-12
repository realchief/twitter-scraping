# -*- coding: utf-8 -*-
import re
import requests
import json
import datetime
import scrapy
import urllib
from scrapy import Request, Field
from lxml import html
from urlparse import urljoin
from datetime import datetime

class TwitterItem(scrapy.Item):
    Author = Field()
    username = Field
    Content = Field()
    TweetCount = Field()
    FollowerCount = Field()
    TwitterTime = Field()
    AuthorLocation = Field()
    RepliesCount = Field()
    RetweetCount = Field()
    LikeCount = Field()


class TwitterSpider(scrapy.Spider):

    name = 'twitter'

    allowed_domains = ["twitter.com"]

    start_urls = ['https://twitter.com/search-home']

    search_url = 'https://twitter.com/search?q={keyword}&src=typd'

    next_page_url = 'https://twitter.com/i/search/timeline?vertical=default&q=Comorbidity&src=typd&' \
                    'include_available_features=1&include_entities=1&max_position={position}&reset_error_state=false'

    # headers = {
    #     # ':authority': 'twitter.com',
    #     # ':method': 'GET',
    #     # ':path': '/i/search/timeline?vertical=default&q=Comorbidity&src=typd&include_available_features=1&include_entities=1&max_position=cm%2B55m-aDFavFIJIJEIbFEvbDv-aDFavFIJIJEIbFEvbDv-BD1UO2FFu9QAAAAAAAAVfAAAAAcAAABWACAAQAAAAAkAAAAAAAAAAAAIAAAABAAAAAAAQAAiAAAAAAAABAAAAAAAAIAAAAAAADAgAgAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAIAAAAAAAQAABAAAAAAQQAAAAAAAAAAAAAAAAAgAgAAAAAAAIAABAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAACAAAAAAAAAAAAAAAACAAAAAAAAACAIEAIBAAAAKAAAAAACAAAAAAAAAAAAAAAABGAAAAAAAAAAAAAQAAGAAAAAAAAIAIAAQAABAAAAAIAAAAAAAAAAAAAAAAAIAAAAAAAAAAAABAAAAAAgAACAAAAAAAIAAAAgAAAAAiAACAAAAAAAAAAAEAAAAAAAAAiAAQAgAAAAAAAAACAAAAQCAAAAAQQCAAAIAAAAAAAAAAAAAAAAAAAgAAAABAAAAAAAAAAAAAAAAAAAgAAAAgAAAAAgAAAAAQIAAEAAAAAAAAAACAEQAAAAAAQAAAAgAAAAAAAABAAAACAAIAAIAAAAAAAAAAAAAAAACAAAAABAAAAAAIAgAAAggIAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAABABACAABAAAAAAAAAAAAQgCAgAAAAgAAAAAAAAEgAAAAAAAAAIQAAAAAAAAAAAAAAgAAAAAAAAAAAgAAAAAAAAAAEAAAAAAAAAAAAAAAAQAAIAAAAAAAAgAAAAAAABAAAIAAACAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAgAgAIAEAAEIAAAAAAAAAAAAAAAAAAAkAAAAAQAAAAAAAAEAAAAAAAAAAAAAQABEAAAAAQAAAAAAAAAAAgAAAAABAAAAAQAAAAAAAAAAAAAAEAgABAAAAAAAAAAAAAAA%3D%3D-R-0-0&reset_error_state=false',
    #     # ':scheme': 'https',
    #     'accept': 'application/json, text/javascript, */*; q=0.01',
    #     'Content-Type': 'application/json; charset=UTF-8',
    #     # 'accept-encoding': 'gzip, deflate, br',
    #     # 'accept-language': 'en-US,en;q=0.9',
    #     # 'cookie': 'personalization_id="v1_TLtQE/mV4pz5lbxvd7RsrQ=="; guest_id=v1%3A154186148278586553; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCPEkG%252F5mAToMY3NyZl9p%250AZCIlYmRmZTI3ODVmMGU2NDYwOTZhZTRlNzYxYmQ4MDBiNjI6B2lkIiU0MmIy%250AZjQxNDJlOWZlYzAzOTc5OGY1NTNiZjJkMjhlNQ%253D%253D--6efa064f49810dce181851a024d8c84a3add3207; _ga=GA1.2.1487314371.1541886688; _gid=GA1.2.777648253.1541886688; eu_cn=1; lang=en; ct0=f466224df9471fe1d73343f14153d65b; tfw_exp=0; _gat=1',
    #     'referer': 'https://twitter.com/search?q=Comorbidity&src=typd',
    #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    #     'x-requested-with': 'XMLHttpRequest',
    #     # 'x-twitter-active-user': 'yes'
    # }

    query_params = {
        'vertical': 'default',
        'q': 'Comorbidity',
        'src': 'typd',
        'include_available_features': '1',
        'include_entities': '1',
        # 'max_position': 'cm+55m-aDFasIEsaJEbvDDIsbF-aDFasIEsaJEbvDDIsbF-BD1UO2FFu9QAAAAAAAAVfAAAAAcAAABWACAAUAAAAAgAAAAEAAAABgAIAAAABAAAAAQAAAAiAAAAAAAABAAAAAAAAIAAAAAAADAgAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAQAABAAAAAAQQAAAAAAAAAAAAAAAAAgAgAAAAAAAIAABAAAAAAAAAAAACEAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAACAAAAAAAAACAAEAIAAAAAKAAAIAACAAAAAAAAAAAAEAAAAEAAAAAAAAAAAAAQAAAAAAAAAIAIAIAAQAAAAAAAAIAAAAAAAAAAAAAAAAAICAAAAAAAAAAABAAAAAAAAACAAAAAAAIAAAAgAAAAAiAACAAAAAAAAAAAEAAAAAAAAAgAAAAgAAAAAAAAACAAAAQCAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAgAAAABACAAAAAAAAAAAAAAAAAEAAAAgAAAAAgAAAAAQAAAEAAAAAAAAAACAAQAAAAAAQAAAAgAAAAAAgABAAAACAAIAAAAAAAAAAIAAAAAAAACAAAAAAAAAAAAIAAAAAggIACAAAAAAIAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAEEAAAAAAAAACAABAAAAAAAAAAAAQgCAAAAAAgAAAAAAAAEAAAAAAAAAAAQAAAAQAAAgAAAAAgAAAAAAAAAIAgAAAAAAAAAAEAAAAAAAAAAEAAAAAQAAAAAAAAAAAAAAAAAACBAAAIAAACAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAACAAAIQEAAEIAAAAAAAAAAAAAgAAAAAkAAAAAAAAAAAAAAEAACAAAAAAAAAAQABEAAAAAQAAAAEAEAAAAgAAAAABAAAAAQAAAAAAAAAAAEAAEQgABACAAAAAAAAAAQAA==-R-0-0',
        'reset_error_state': 'false'
    }
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
               }

    token = None

    refer = None

    def __init__(self, *args, **kwargs):
        super(TwitterSpider, self).__init__(site_name=self.allowed_domains[0], *args, **kwargs)
        self.current_page = 0

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        keyword = 'Comorbidity'
        search_url = self.search_url.format(keyword=keyword)
        self.refer = search_url
        yield Request(url=search_url, callback=self.parse_twitter_page, headers=self.headers)

    def parse_twitter_page(self, response):
        next_page = None
        if self.current_page == 0:
            posts = response.xpath('//li[@data-item-type="tweet"]').extract()
            min_position = re.search('data-min-position="(.*?)"', response.body)
            if min_position:
                min_position = min_position.group(1)
            next_page = self.next_page_url.format(position=min_position.replace('cm+', 'cm%2B').replace('==', '%3D%3D'))
            self.query_params['max_position'] = min_position

            token = str(response.xpath('//input[@name="authenticity_token"]/@value').extract()[0])
            self.token = token

            for post in posts:
                time_stamp = int(html.fromstring(post).xpath('//small[@class="time"]/a/span/@data-time')[0])
                twitter_time = datetime.fromtimestamp(time_stamp).strftime("%Y-%m-%d %H:%M:%S")
                post_year = int(datetime.fromtimestamp(time_stamp).strftime("%Y"))
                current_year = datetime.now().year
                if post_year < int(current_year) - 2:
                    next_page = None
                    break
                author = self._clean_text(html.fromstring(post).xpath('//span[@class="FullNameGroup"]/strong/text()')[0])
                content = self._clean_text(' '.join(html.fromstring(post)
                                                    .xpath('//p[contains(@class, "TweetTextSize")]/text()')))

                replies_count = html.fromstring(post).xpath\
                    ('//div[contains(@class, "ProfileTweet-action--reply")]'
                    '//span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(replies_count) > 0:
                    replies_count = int(replies_count[0])
                else:
                    replies_count = 0

                retweet_count = html.fromstring(post).xpath\
                    ('//div[contains(@class, "ProfileTweet-action--retweet")]'
                    '//span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(retweet_count) > 0:
                    retweet_count = int(retweet_count[0])
                else:
                    retweet_count = 0

                like_count = html.fromstring(post).xpath\
                    ('//div[contains(@class, "ProfileTweet-action--favorite")]//'
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

                meta = response.meta.copy()
                meta['twitter'] = twitter

                author_link = urljoin(response.url, html.fromstring(post)
                                       .xpath('//div[@class="stream-item-header"]/a/@href')[0])
                if author_link:
                     yield Request(
                        url=author_link,
                        callback=self.parse_author,
                        meta=meta,
                        headers=self.headers,
                        dont_filter=True
                    )

            self.headers['refer'] = self.refer
            self.current_page = 1
        else:
            json_data = json.loads(response.body)
            min_position = json_data.get('min_position')

        if next_page:
            yield scrapy.http.Request(
                url=self.next_page_url,
                # method='POST',
                # body=json.dumps(self.query_params),
                callback=self.parse_twitter_page,
                headers=self.headers,
                # cookies=self.token
            )

    def parse_author(self, response):
        meta = response.meta
        twitter = meta['twitter']
        tweet_count = int(response.xpath('//li[contains(@class, "ProfileNav-item--tweets is-active")]//span[@class="ProfileNav-value"]/@data-count').extract()[0])
        follower_count = int(response.xpath('//li[contains(@class, "ProfileNav-item--followers")]//span[@class="ProfileNav-value"]/@data-count').extract()[0])
        author_location = self._clean_text(response.xpath('//span[contains(@class, "ProfileHeaderCard-locationText")]/text()').extract()[0])

        twitter['TweetCount'] = tweet_count
        twitter['FollowerCount'] = follower_count
        twitter['AuthorLocation'] = author_location

        return twitter

    @staticmethod
    def _clean_text(text):
        text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
        text = re.sub("&nbsp;", " ", text).strip()

        return re.sub(r'\s+', ' ', text)