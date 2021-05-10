import datetime
import re


def get_news_headline(soup_text):
    """

    :param soup_text:
    :return:
    """
    title = soup_text.find('title')
    if title:
        return title.string


def parse_date(date_str):
    """

    :param date_str:
    :return:
    """
    # pymongo uses datetime.datetime objects for representing dates in mongo docs
    posted_date = datetime.datetime.strptime(date_str, '%b %d, %Y')
    return posted_date


def is_article(soup_text):
    """

    :param soup_text:
    :return:
    """
    article = soup_text.find_all('article')
    # if its a page with new article, it should contain
    # only one <article> tag
    if len(article) == 1:
        return True
    else:
        return False


def get_posted_date(soup_text):
    """

    :param soup_text:
    :return:
    """
    time_tag = soup_text.find('time')
    # 2 cases, either date text is inside <b> tag or it is not.
    # we have to handle both cases here
    if time_tag:
        b_tag = time_tag.find('b')
        if b_tag:
            posted_date_str = b_tag.text.strip()
            posted_date = parse_date(posted_date_str)
        else:
            posted_date_str = time_tag.text.strip()
            posted_date = parse_date(posted_date_str)
        return posted_date


def get_news_author(soup_text):
    """

    :param soup_text:
    :return:
    """
    # author has link of pattern https://author/
    anchor_tag = soup_text.find('a', href=re.compile("https:.*/author/.*"))
    if anchor_tag:
        author = anchor_tag.text
        return author
