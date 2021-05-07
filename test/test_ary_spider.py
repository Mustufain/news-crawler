import os
import unittest
from news_crawler.spiders.ary_spider import AryNewsSpider
import datetime
from news_crawler.test.utils import fake_response
from unittest.mock import patch, mock_open


class AryNewsSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = AryNewsSpider()
        self.date_str = 'May 4, 2018'
        self.valid_response = fake_response('data/news.html')
        self.invalid_response = fake_response('data/sports.html')

    def test_parse_date(self):
        posted_date = self.spider.parse_date(self.date_str)
        target_date = datetime.datetime(2018, 5, 4).date()
        self.assertEqual(posted_date, target_date)

    def test_get_valid_news_author(self):
        author = self.spider.get_news_author(self.valid_response)
        self.assertEqual(author, 'Web Desk')

    def test_get_invalid_news_author(self):
        author = self.spider.get_news_author(self.invalid_response)
        self.assertEqual(author, '')

    def test_get_valid_posted_date(self):

        posted_date = self.spider.get_posted_date(self.valid_response)
        self.assertEqual(posted_date, datetime.datetime(2021, 5, 4).date())

    def test_get_invalid_posted_date(self):
        posted_date = self.spider.get_posted_date(self.invalid_response)
        self.assertEqual(posted_date, '')

    def test_get_empty_visited_urls(self):
        self.spider.filename = 'foo.txt'
        self.spider.get_visited_urls()
        self.assertEqual(self.spider.urls_visited, [])

    def test_get_visited_urls(self):
        base_path = os.getcwd()
        file_path = os.path.join(base_path, 'test/data/test_url_visited.txt')
        self.spider.filename = file_path
        self.spider.get_visited_urls()
        self.assertEqual(len(self.spider.urls_visited), 3)

    def test_parse_items(self):
        with patch('builtins.open', new_callable=mock_open()) as m:
            item = next(self.spider.parse_items(self.valid_response))
            # simple assertion that your open was called with append
            file = os.path.join(os.getcwd(), 'spiders/url_visited.txt')
            m.assert_called_with(file, 'a')
            self.assertEqual(item['url'], 'http://www.example.com')
            self.assertEqual(item['author'], 'Web Desk')
            self.assertEqual(item['posted_date'], datetime.datetime(2021, 5, 4).date())

    def test_get_news_headline(self):
        news_headline = self.spider.get_news_headline(self.valid_response)
        sports_headline = self.spider.get_news_headline(self.invalid_response)
        assert news_headline is not None
        assert sports_headline is not None
