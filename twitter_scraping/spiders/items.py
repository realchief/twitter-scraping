import scrapy
from scrapy import Field

class TwitterItem(scrapy.Item):
    Author = Field()
    Username = Field()
    Content = Field()
    TweetCount = Field()
    FollowerCount = Field()
    TwitterTime = Field()
    AuthorLocation = Field()
    RepliesCount = Field()
    RetweetCount = Field()
    LikeCount = Field()