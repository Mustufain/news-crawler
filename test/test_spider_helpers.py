import datetime
import unittest
import mock
from bs4 import BeautifulSoup
from news_crawler.spiders.spider_helpers import is_article, \
    get_posted_date, get_news_headline, \
    get_time_tag, get_news_author, if_url_exists
from .utils import fake_response


class SpiderHelpers(unittest.TestCase):
    def setUp(self):
        self.date_str = 'May 4, 2018'
        self.news_soup = BeautifulSoup(
            fake_response('data/news.html').text, 'lxml')
        self.sports_soup = BeautifulSoup(
            fake_response('data/sports.html').text, 'lxml')
        self.invalid_soup = BeautifulSoup(
            fake_response('data/invalid_response.html').text, 'lxml')
        self.invalid_sports_soup = BeautifulSoup(
            fake_response('data/invalid_sports_text.html').text, 'lxml')

    def test_get_time_tag(self):
        news_time_tag = get_time_tag(self.news_soup)
        sports_time_tag = get_time_tag(self.sports_soup)
        invalid_time_tag = get_time_tag(self.invalid_soup)
        assert news_time_tag is not None
        assert sports_time_tag is not None
        assert invalid_time_tag is None

    def test_get_news_posted_date(self):
        posted_date = get_posted_date(self.news_soup.find('time'))
        self.assertEqual(posted_date, datetime.datetime(2021, 5, 4))

    def test_get_sports_posted_date(self):

        posted_date = get_posted_date(self.sports_soup.find('time'))
        self.assertEqual(posted_date, datetime.datetime(2021, 5, 5))

    def test_get_sports_invalid_posted_date(self):
        posted_date = get_posted_date(self.invalid_sports_soup.find('time'))
        self.assertEqual(posted_date, datetime.datetime(2021, 1, 17))

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
        anchor_tag = get_news_author(self.news_soup)
        self.assertEqual(anchor_tag.text, 'Web Desk')

    def test_get_sports_news_author(self):
        anchor_tag = get_news_author(self.sports_soup)
        self.assertEqual(anchor_tag.text, 'Shoaib Jatt')

    def test_get_empty_news_author(self):
        anchor_tag = get_news_author(self.invalid_soup)
        assert anchor_tag is None

    @mock.patch("pymongo.MongoClient")
    def test_if_url_exists(self, mock_pymongo):
        if_url_exists('foo')
        self.assertTrue(mock_pymongo.called)
