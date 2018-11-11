import scrapy
from scrapy import Request, Field
from lxml import html
from urlparse import urljoin
from datetime import datetime
import re
import collections


class TwitterAccountItem(scrapy.Item):
    Author = Field()
    Content = Field()
    FollowCount = Field
    TwitterTime = Field()
    AccountName = Field()
    RepliesCount = Field()
    TweetCount = Field()
    LikeCount = Field()


class TwitterAccountSpider(scrapy.Spider):

    name = 'twitter'
    allowed_domains = ["twitter.com"]
    start_urls = ['https://twitter.com/search-home']
    search_url = 'https://twitter.com/search?q={keyword}&src=typd'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/41.0.2228.0 Safari/537.36', }

    def __init__(self, *args, **kwargs):
        super(TwitterAccountSpider, self).__init__(site_name=self.allowed_domains[0], *args, **kwargs)
        self.current_page = 0

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_search_page, headers=self.headers)

    def parse_search_page(self, response):
        keyword = 'Comorbidity'
        search_url = self.search_url.format(keyword=keyword)
        yield Request(url=search_url, callback=self.parse_twitter_page, headers=self.headers)

    def parse_twitter_page(self, response):
        posts = response.xpath('//div[@class="stream"]/ol[contains(@class, "stream-items")]/li').extract()
        for post in posts:
            author = self._clean_text(html.fromstring(post).xpath('//span[@class="FullNameGroup"]/strong/text()')[0])
            account_link = urljoin(response.url, html.fromstring(post)
                                   .xpath('//div[@class="stream-item-header"]/a/@href')[0])
            content = self._clean_text(' '.join(html.fromstring(post)
                                                .xpath('//p[contains(@class, "TweetTextSize")]/text()')))
            twitter_time =
            replies_count = 0
            retweet_count = 0
            like_count = 0
            try:
                replies_count = html.fromstring(post).xpath\
                    ('//div[contains(@class, "ProfileTweet-action--reply")]'
                    '//span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(replies_count) > 0:
                    replies_count = int(replies_count[0])

                retweet_count = html.fromstring(post).xpath\
                    ('//div[contains(@class, "ProfileTweet-action--retweet")]'
                    '//span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(retweet_count) > 0:
                    retweet_count = int(retweet_count[0])

                like_count = html.fromstring(post).xpath\
                    ('//div[contains(@class, "ProfileTweet-action--favorite")]//'
                    'span[@class="ProfileTweet-actionCountForPresentation"]/text()')
                if len(like_count) > 0:
                    like_count = int(like_count[0])
            except:
                pass


    def _clean_text(self, text):
        text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
        text = re.sub("&nbsp;", " ", text).strip()

        return re.sub(r'\s+', ' ', text)