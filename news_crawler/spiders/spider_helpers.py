import datetime
import re
from bs4 import BeautifulSoup
from scrapy.utils.project import get_project_settings
import pymongo


def get_news_headline(soup_text: BeautifulSoup) -> BeautifulSoup:
    """

    :param soup_text:
    :return:
    """
    title = soup_text.find('title')
    return title


def get_posted_date(time_tag: BeautifulSoup) -> datetime:
    """

    :param time_tag:
    :return:
    """
    # 2 cases, either date text is inside <b> tag or it is not.
    # we have to handle both cases here
    b_tag = time_tag.find('b')
    if b_tag:
        date_str = b_tag.text.strip()
    else:
        date_str = time_tag.text.strip()
    # pymongo uses datetime.datetime objects
    # for representing dates in mongo docs
    # There are two date patterns:
    # %b %d, %Y and %B %d, %Y
    if len(date_str.split(' ')[0]) == 3:
        # month is in short form (3 characters eg: Sep)
        posted_date = datetime.datetime.strptime(
            date_str, '%b %d, %Y')
    else:
        posted_date = datetime.datetime.strptime(
            date_str, '%B %d, %Y')

    return posted_date


def is_article(soup_text: BeautifulSoup) -> bool:
    """

    :param soup_text:
    :return:
    """
    article = soup_text.find_all('article')
    # if its a page with new article, it should contain
    # only one <article> tag
    return bool(len(article) == 1)


def get_time_tag(soup_text: BeautifulSoup) -> datetime:
    """

    :param soup_text:
    :return:
    """
    time_tag = soup_text.find('time')
    return time_tag


def get_news_author(soup_text: BeautifulSoup) -> BeautifulSoup:
    """

    :param soup_text:
    :return:
    """
    # author has link of pattern https://author/
    anchor_tag = soup_text.find(
        'a', href=re.compile("https:.*/author/.*"))
    return anchor_tag


def get_visited_urls() -> list:
    url_visited = []
    settings = get_project_settings()
    uri = settings['MONGODB_URI']
    database = settings['MONGODB_DB']
    mongo_client = pymongo.MongoClient(uri)
    mongo_db = mongo_client[database]
    for row in mongo_db['news_articles'].find(
            {}, {"_id": 0, "url": 1}):
        url_visited.append(row['url'])
    return url_visited
