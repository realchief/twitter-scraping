# Twitter Scraper Instllation Guide

## Retrieve code

* `$ https://github.com/realchief/twitter-scraping.git`

## Create Vritual Environment

* `$ sudo apt-get install python-virtualenv`
* `$ cd twitter_scraping`
* `$ virtualenv venv`
* `$ source venv/bin/activate`


## Install packages

* `$ pip install -r requirements.txt`


## Run spiders

* `$ cd twitter_scraping/spiders`
* `$ scrapy crawl twitter -o result.json`
* `$ scrapy crawl swedish_twitter -o swedish_twitter_result.json`
* `$ scrapy crawl danish_twitter -o danish_twitter_result.json`
* `$ scrapy crawl norwegian_twitter -o norwegian_twitter_result.json`


# Check all generated json
