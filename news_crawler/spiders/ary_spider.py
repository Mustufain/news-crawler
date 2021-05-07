import os
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news_crawler.items import NewsItem


class AryNewsSpider(CrawlSpider):
    name = "ary"
    rules = [Rule(
        LinkExtractor(
            deny=['category/', 'author/', 'videos.arynews.tv']
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
        self.filename = os.path.join(os.getcwd(), 'spiders/url_visited.txt')
        self.posted_date_xpath = '//time[@class="post-published updated"]/b/text()'
        self.author_xpath = '//a[@class="author url fn"]/text()'
        self.title_xpath = '/html/head/title/text()'
        self.post_xpath = '//div[@class="post-header post-tp-1-header"]'
        self.start_urls = ['http://arynews.tv']
        super().__init__()

    def get_news_headline(self, response):
        """

        :param response:
        :return:
        """
        title = response.xpath(self.title_xpath).get()
        return title

    def get_news_author(self, response):
        """

        :param response:
        :return:
        """
        author = response.xpath(self.author_xpath).get()
        if author:
            return author.strip()
        else:
            return ''

    def get_posted_date(self, response):
        """

        :param response:
        :return:
        """
        date_str = response.xpath(self.posted_date_xpath).get()
        if date_str:
            posted_date = self.parse_date(date_str)
            return posted_date
        else:
            return ''

    @staticmethod
    def parse_date(date_str):
        """

        :param date_str:
        :return:
        """
        posted_date = datetime.datetime.strptime(date_str, '%b %d, %Y').date()
        return posted_date

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
        exists = response.xpath(self.post_xpath).extract_first()
        if exists:  # if post exists
            if response.url not in self.urls_visited:
                # scrapping logic here
                news_item = NewsItem()
                news_item['url'] = response.url
                news_item['author'] = self.get_news_author(response)
                news_item['posted_date'] = self.get_posted_date(response)
                headline = self.get_news_headline(response)
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
