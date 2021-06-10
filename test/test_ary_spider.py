import unittest
import datetime
from news_crawler.spiders.ary_spider import AryNewsSpider
from .utils import fake_response


class AryNewsSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = AryNewsSpider(ds='2020-10-01')
        self.news_response = fake_response('data/news.html')
        self.sports_response = fake_response('data/sports.html')
        self.invalid_response = fake_response('data/invalid_response.html')

    def test_parse_news_items(self):
        item = next(self.spider.parse_attr(self.news_response))
        self.assertEqual(item['url'], 'http://www.example.com')
        self.assertEqual(item['author'], 'Web Desk')
        self.assertEqual(item['posted_date'],
                         datetime.datetime(2021, 5, 4))
        assert item['headline'] is not None

    def test_parse_sports_items(self):
        item = next(self.spider.parse_attr(self.sports_response))
        self.assertEqual(item['url'], 'http://www.example.com')
        self.assertEqual(item['author'], 'Shoaib Jatt')
        self.assertEqual(item['posted_date'],
                         datetime.datetime(2021, 5, 5))
        assert item['headline'] is not None
