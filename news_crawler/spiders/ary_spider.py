import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_crawler.items import NewsItem
from bs4 import BeautifulSoup
from news_crawler.spiders.spider_helpers import is_article, \
    get_posted_date, get_news_headline, get_news_author


class AryNewsSpider(CrawlSpider):
    name = "ary"
    rules = [Rule(
        LinkExtractor(
            allow=["arynews.tv/en/*", "https://arysports.tv/*"]  # only such urls
        ),
        callback='parse_items',
        follow=True
    )
    ]
    custom_settings = {
        'LOG_LEVEL': 'INFO',
    }

    def __init__(self):

        self.urls_visited = []
        self.filename = os.path.join(os.getcwd(), 'news_crawler/spiders/url_visited.txt')
        # self.author_regex = r">([^<]*)</a>"
        self.start_urls = ['https://arynews.tv/en']
        super().__init__()

    def get_visited_urls(self):
        """

        :return:
        """
        try:
            with open(self.filename) as urls:
                self.urls_visited = urls.read().splitlines()
        except FileNotFoundError:
            # File not found, it means we are scraping for the first time
            pass

    def parse_items(self, response):
        """

        :param response:
        """
        self.get_visited_urls()
        soup = BeautifulSoup(response.text, 'lxml')
        article_exists = is_article(soup)
        if article_exists:
            if response.url not in self.urls_visited:
                # scrapping logic here
                news_item = NewsItem()
                news_item['url'] = response.url
                news_item['text'] = response.text
                author = get_news_author(soup)
                posted_date = get_posted_date(soup)
                headline = get_news_headline(soup)
                if author:
                    news_item['author'] = author
                if posted_date:
                    news_item['posted_date'] = posted_date
                if headline:
                    news_item['headline'] = headline
                # append url to file
                with open(self.filename, "a") as urls_visited:
                    urls_visited.write(response.url + "\n")
                yield news_item
            else:
                self.logger.info('url %s has already been visited', response.url)
        else:
            self.logger.info('url %s does not contain news post', response.url)
