from scrapy.spiders import CrawlSpider
from scrapy import Request
from bs4 import BeautifulSoup

from news_crawler.items import NewsItem
from news_crawler.spiders.spider_helpers import is_article, \
    get_posted_date, get_news_headline, get_news_author, \
    get_time_tag, extract_url, if_url_exists, get_next_url


class AryNewsSpider(CrawlSpider):
    name = "ary"
    custom_settings = {
        'LOG_LEVEL': 'INFO',
    }

    def start_requests(self):
        urls = ['https://arynews.tv/en/2017/05/10/',
                'https://arysports.tv/2017/05/10/']
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        """

        :param response:
        """
        # here we receive the contents of the page:
        # https://arysports.tv|arynews.tv/YYYY/MM/DD/
        self.logger.info(response.url)
        soup = BeautifulSoup(response.text, 'lxml')
        page_urls = extract_url(soup, response.url)
        if page_urls:
            self.logger.info(page_urls)
            for url in page_urls:
                url_exists = if_url_exists(url)
                if url_exists:
                    self.logger.info('url already scraped: %s', url)
                else:
                    self.logger.info('processing url %s', url)
                    yield Request(url, callback=self.parse_attr)
            next_url = get_next_url(soup, response.url)
            if next_url:
                self.logger.info('next_url: %s', next_url)
                yield Request(next_url, callback=self.parse)
            else:
                self.logger.info('scrapper reached at the end of page')
        else:
            self.logger.info('urls cannot be extracted')

    def parse_attr(self, response):
        """
        parses each url
        :param response:
        :return:
        """
        soup = BeautifulSoup(response.text, 'lxml')
        article_exists = is_article(soup)
        if article_exists:
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
                'url %s does not contain news post',
                response.url)
