import datetime
import unittest
from .utils import fake_response
from bs4 import BeautifulSoup
from news_crawler.spiders.spider_helpers import is_article, \
    get_posted_date, get_news_headline, \
    parse_date, get_news_author


class SpiderHelpers(unittest.TestCase):
    def setUp(self):
        self.date_str = 'May 4, 2018'
        self.news_soup = BeautifulSoup(fake_response('data/news.html').text, 'lxml')
        self.sports_soup = BeautifulSoup(fake_response('data/sports.html').text, 'lxml')
        self.invalid_soup = BeautifulSoup(fake_response('data/invalid_response.html').text, 'lxml')

    def test_parse_date(self):
        posted_date = parse_date(self.date_str)
        target_date = datetime.datetime(2018, 5, 4)
        self.assertEqual(posted_date, target_date)

    def test_get_posted_date(self):
        posted_date = get_posted_date(self.news_soup)
        self.assertEqual(posted_date, datetime.datetime(2021, 5, 4))

    def test_get_sports_posted_date(self):
        posted_date = get_posted_date(self.sports_soup)
        self.assertEqual(posted_date, datetime.datetime(2021, 5, 5))

    def test_empty_posted_date(self):
        posted_date = get_posted_date(self.invalid_soup)
        assert posted_date is None

    def test_get_news_headline(self):
        news_headline = get_news_headline(self.news_soup)
        sports_headline = get_news_headline(self.sports_soup)
        assert news_headline is not None
        assert sports_headline is not None

    def test_is_article(self):
        new_article = is_article(self.news_soup)
        assert new_article is True

        sports_article = is_article(self.sports_soup)
        assert sports_article is True

    def test_is_not_article(self):
        article = is_article(self.invalid_soup)
        assert article is False

    def test_get_news_author(self):
        author = get_news_author(self.news_soup)
        self.assertEqual(author, 'Web Desk')

    def test_get_sports_news_author(self):
        author = get_news_author(self.sports_soup)
        self.assertEqual(author, 'Shoaib Jatt')

    def test_get_empty_news_author(self):
        author = get_news_author(self.invalid_soup)
        assert author is None
