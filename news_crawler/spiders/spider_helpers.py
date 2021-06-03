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


def if_url_exists(url: str) -> bool:
    settings = get_project_settings()
    uri = settings['MONGODB_URI']
    database = settings['MONGODB_DB']
    mongo_client = pymongo.MongoClient(uri)
    mongo_db = mongo_client[database]
    visited_url = mongo_db['news_articles'].find_one(
        {"url": url})
    if visited_url:
        return True
    else:
        return False


def extract_news_url(soup_text: BeautifulSoup, url_pattern: str) -> list:
    """
    Extract url of the articles from html text
    :param url_pattern:
    :param soup_text:
    :return:
    """
    page_urls = []
    exclude_pattern = "https://arynews.tv/en/category"
    articles = soup_text.find_all('article')
    for article in articles:
        # get all links in article
        for link in article.findAll(
                'a', attrs={'href': re.compile(url_pattern)}):
            url = link.get('href')
            if exclude_pattern not in url:
                page_urls.append(url)
    if len(page_urls) > 0:
        unique_urls = list(set(page_urls))
    else:
        unique_urls = None
    return unique_urls


def extract_sports_url(soup_text: BeautifulSoup, url_pattern: str):
    page_urls = []
    main_div = soup_text.find("div",
                              {"class": "td-pb-span8 td-main-content"})
    div_with_link = main_div.find_all("div",
                                      {"class": "td-module-thumb"})
    for div in div_with_link:
        url = div.find(
            'a', attrs={'href': re.compile(url_pattern)}).get('href')
        page_urls.append(url)
        unique_urls = list(set(page_urls))
    return unique_urls


def get_next_url(soup_text: BeautifulSoup, url: str):
    news_pattern = "https://arynews.tv/en/\d{4}\/\d{2}\/\d{2}\/page\/\d+\/"
    sports_pattern = "https://arysports.tv/\d{4}\/\d{2}\/\d{2}\/page\/\d+\/"
    if 'arysports.tv' in url:
        next_url = soup_text.find(
            'a',
            attrs={
                'href': re.compile(sports_pattern)
            })
        # check if there is next page
        if next_url:
            next_url_link = next_url.get('href')
        else:
            next_url_link = None
    elif "arynews.tv" in url:
        next_url = soup_text.find(
            'a',
            attrs={
                'href': re.compile(news_pattern)
            })
        if next_url:
            next_url_link = next_url.get('href')
        else:
            next_url_link = None
    else:
        next_url_link = None
    return next_url_link


def extract_url(soup_text: BeautifulSoup, url: str):
    if 'arysports.tv' in url:
        page_urls = extract_sports_url(soup_text, "^https://arysports.tv/")
    elif "arynews.tv" in url:
        page_urls = extract_news_url(soup_text, "^https://arynews.tv/")
    else:
        page_urls = None
    return page_urls
