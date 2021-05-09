import unittest
from scrapy.spiders import Spider
from news_crawler.items import NewsItem
from news_crawler.pipelines import NewsTextPipeline, \
    NewsPlaceMentionedPipeline, DropEmptyRequiredFieldsPipeline, \
    DuplicatesPipeline, MongoPipeline
from .utils import fake_response, read_file
import mock
from nose.tools import raises


class NewsTextPipelineTest(unittest.TestCase):

    def setUp(self):
        self.spider = Spider(name='spider')
        self.news_response = fake_response("data/news.html")
        self.sports_response = fake_response('data/sports.html')
        self.pipeline = NewsTextPipeline()
        self.item = NewsItem()

    def test_process_item(self):
        self.item['text'] = self.news_response.text
        news = self.pipeline.process_item(self.item, self.spider)
        text = read_file('data/news_text.txt')
        self.assertEqual(news['text'], text)

        self.item['text'] = self.sports_response.text
        sports = self.pipeline.process_item(self.item, self.spider)
        text = read_file('data/sports_text.txt')
        self.assertEqual(sports['text'], text)


class NewsPlaceMentionedPipelineTest(unittest.TestCase):

    def setUp(self):
        self.spider = Spider(name='spider')
        self.pipeline = NewsPlaceMentionedPipeline()
        self.item = NewsItem()

    @mock.patch('geograpy.extraction.Extractor')
    def test_process_item(self, mock_extractor):
        mock_extractor.return_value.places = ['Islamabad']
        self.item['url'] = 'https://arynews.tv/en/imran-khan-labour-day-workers/'
        item = self.pipeline.process_item(self.item, self.spider)
        self.assertTrue(mock_extractor.return_value.find_geoEntities.called)
        self.assertEqual(item['places_mentioned'], ['Islamabad'])


class DropEmptyRequiredFieldsPipelineTest(unittest.TestCase):

    def setUp(self):
        self.spider = Spider(name='spider')
        self.item = NewsItem()
        self.pipeline = DropEmptyRequiredFieldsPipeline()

    def test_process_item(self):
        self.item['headline'] = 'fooheadline'
        self.item['text'] = 'footext'
        self.item['author'] = 'fooauthor'
        self.item['url'] = 'foourl'
        item = self.pipeline.process_item(self.item, self.spider)
        assert item is not None

    @raises(Exception)
    def test_missing_url_process_item(self):
        self.item['headline'] = 'fooheadline'
        self.item['text'] = 'footext'
        self.item['author'] = 'fooauthor'
        self.pipeline.process_item(self.item, self.spider)

    @raises(Exception)
    def test_missing_headline_process_item(self):
        self.item['text'] = 'footext'
        self.item['author'] = 'fooauthor'
        self.item['url'] = 'foourl'
        self.pipeline.process_item(self.item, self.spider)


class DuplicatesPipelineTest(unittest.TestCase):

    def setUp(self):
        self.pipeline = DuplicatesPipeline()
        self.spider = Spider(name='spider')
        self.item = NewsItem()

    @raises(Exception)
    def test_duplicate_process_items(self):
        self.pipeline.url_seen.add('foourl')
        self.item['url'] = 'foourl'
        self.pipeline.process_item(self.item, self.spider)

    def test_unique_process_items(self):
        self.item['headline'] = 'fooheadline'
        self.item['text'] = 'footext'
        self.item['author'] = 'fooauthor'
        self.item['url'] = 'exampleurl'
        item = self.pipeline.process_item(self.item, self.spider)
        target = set()
        target.add('exampleurl')
        actual_value = list(self.pipeline.url_seen.union(target))[0]
        assert item is not None
        self.assertEqual(actual_value, 'exampleurl')


class MongoPipelineTest(unittest.TestCase):

    def setUp(self):
        self.pipeline = MongoPipeline('mongo_uri', 'mongo_db')
        self.spider = Spider(name='spider')
        self.item = NewsItem()

    @mock.patch("pymongo.MongoClient")
    def test_open_spider(self, mock_pymongo):
        self.pipeline.open_spider(self.spider)
        self.assertTrue(mock_pymongo.called)

    @mock.patch("news_crawler.pipelines.MongoPipeline.insert")
    def test_process_item(self, mock_insert):
        self.item['url'] = 'foourl'
        self.pipeline.process_item(self.item, self.spider)
        self.assertTrue(mock_insert.called)
