import sys
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from news_crawler.spiders.ary_spider import AryNewsSpider
from news_crawler.utils import if_tagger_exists, if_tokenizer_exists, \
    if_chunker_exists, if_corpora_exists

if __name__ == '__main__':
    date_str = sys.argv[1]
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise Exception('date should be of format: YYYY-MM-dd')
    if_tokenizer_exists()
    if_tagger_exists()
    if_chunker_exists()
    if_corpora_exists()
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(AryNewsSpider, ds=date_str)
    process.start()
