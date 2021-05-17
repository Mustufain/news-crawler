from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from news_crawler.items import NewsItem
from news_crawler.spiders.spider_helpers import is_article, \
    get_posted_date, get_news_headline, get_news_author, \
    get_time_tag, get_visited_urls


class AryNewsSpider(CrawlSpider):
    name = "ary"
    rules = [Rule(
        LinkExtractor(
            allow=["arynews.tv/en/*",
                   "https://arysports.tv/*"],  # only such urls
            deny=['/category', '/author', '/page']
        ),
        callback='parse_items',
        follow=True
    )
    ]
    custom_settings = {
        'LOG_LEVEL': 'INFO',
    }

    def __init__(self):

        self.start_urls = ['https://arynews.tv/en', 'https://arysports.tv/']
        self.allowed_domains = ["arynews.tv", "arysports.tv"]
        self.urls_visited = get_visited_urls()
        super().__init__()

    def parse_items(self, response):
        """

        :param response:
        """
        soup = BeautifulSoup(response.text, 'lxml')
        article_exists = is_article(soup)
        if article_exists:
            if response.url not in self.urls_visited:
                # scrapping logic here
                news_item = NewsItem()
                news_item['url'] = response.url
                news_item['text'] = response.text
                anchor_tag = get_news_author(soup)
                time_tag = get_time_tag(soup)
                title_tag = get_news_headline(soup)
                # if anchor tag is found
                if anchor_tag:
                    news_item['author'] = anchor_tag.text
                # if time tag is found
                if time_tag:
                    posted_date = get_posted_date(time_tag)
                    news_item['posted_date'] = posted_date
                # if title tag is found
                if title_tag:
                    news_item['headline'] = title_tag.text
                yield news_item
            else:
                self.logger.info(
                    'url %s has already been visited',
                    response.url)
        else:
            self.logger.info(
                'url %s does not contain news post',
                response.url)
