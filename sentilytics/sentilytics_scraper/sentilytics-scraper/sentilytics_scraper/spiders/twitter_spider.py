import scrapy


class TwitterSpiderSpider(scrapy.Spider):
    name = "twitter_spider"
    allowed_domains = ["twitter.com"]
    start_urls = ["https://twitter.com"]

    def parse(self, response):
        pass
