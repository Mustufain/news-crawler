import os
import unittest
from news_crawler.spiders.ary_spider import AryNewsSpider
import datetime
from .utils import fake_response
from unittest.mock import patch, mock_open


class AryNewsSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = AryNewsSpider()
        self.news_response = fake_response('data/news.html')
        self.sports_response = fake_response('data/sports.html')
        self.invalid_response = fake_response('data/invalid_response.html')

    def test_get_empty_visited_urls(self):
        self.spider.filename = 'invalid_response.html'
        self.spider.get_visited_urls()
        self.assertEqual(self.spider.urls_visited, [])

    def test_get_visited_urls(self):
        base_path = os.getcwd()
        file_path = os.path.join(base_path, 'test/data/test_url_visited.txt')
        self.spider.filename = file_path
        self.spider.get_visited_urls()
        self.assertEqual(len(self.spider.urls_visited), 3)

    def test_parse_news_items(self):
        with patch('builtins.open', new_callable=mock_open()) as m:
            item = next(self.spider.parse_items(self.news_response))
            # simple assertion that your open was called with append
            file = os.path.join(os.getcwd(), 'news_crawler/spiders/url_visited.txt')
            m.assert_called_with(file, 'a')
            self.assertEqual(item['url'], 'http://www.example.com')
            self.assertEqual(item['author'], 'Web Desk')
            self.assertEqual(item['posted_date'], datetime.datetime(2021, 5, 4))
            assert item['headline'] is not None

    def test_parse_sports_items(self):
        with patch('builtins.open', new_callable=mock_open()) as m:
            item = next(self.spider.parse_items(self.sports_response))
            # simple assertion that your open was called with append
            file = os.path.join(os.getcwd(), 'news_crawler/spiders/url_visited.txt')
            m.assert_called_with(file, 'a')
            self.assertEqual(item['url'], 'http://www.example.com')
            self.assertEqual(item['author'], 'Shoaib Jatt')
            self.assertEqual(item['posted_date'], datetime.datetime(2021, 5, 5))
            assert item['headline'] is not None
