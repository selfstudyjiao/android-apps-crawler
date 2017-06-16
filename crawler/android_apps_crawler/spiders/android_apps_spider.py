import re
import logging

# from scrapy.spiders import Spider
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import HtmlResponse

try:
   import urlparse
except ImportError:
   import urllib.parse as urlparse
try:
   from urlparse import urljoin
except ImportError:
   from urllib.parse import urljoin


from android_apps_crawler.items import AppItem
from android_apps_crawler import settings
from android_apps_crawler import custom_parser


class AndroidAppsSpider(CrawlSpider):
    name = "android_apps_spider"
    scrape_rules = settings.SCRAPE_RULES
    rules = (
        Rule(LinkExtractor(allow = ("http://apk\.hiapk\.com/appinfo",)), callback = 'parse_item', follow = True),
    )

    def __init__(self, market=None, database_dir="../repo/databases/", *args, **kwargs):
        super(AndroidAppsSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = settings.ALLOWED_DOMAINS[market]
        self.start_urls = settings.START_URLS[market]
        settings.MARKET_NAME = market
        settings.DATABASE_DIR = database_dir
        # self.rules = (
        #     Rule(LinkExtractor(allow=settings.CRAWL_RULES[market]), callback = 'parse_item', follow = True),
        # )

    def parse_item(self, response):
        response_domain = urlparse.urlparse(response.url).netloc
        appItemList = []
        cookie = {}
        xpath_rule = self.scrape_rules['xpath']
        for key in xpath_rule.keys():
            if key in response_domain:
                appItemList.extend(
                        self.parse_xpath(response, xpath_rule[key]))
                break
        custom_parser_rule = self.scrape_rules['custom_parser']
        for key in custom_parser_rule.keys():
            if key in response_domain:
                appItemList.extend(
                        getattr(custom_parser, custom_parser_rule[key])(response))
                break

        for item in appItemList:
            yield item


    def parse_xpath(self, response, xpath):
        appItemList = []
        sel = Selector(response)
        for url in response.xpath(xpath).extract():
            url = urljoin(response.url, url)
            logging.info("Catch an application: %s", url)
            appItem = AppItem()
            appItem['url'] = url
            appItemList.append(appItem)
        return appItemList
