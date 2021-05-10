import scrapy


class NewsItem(scrapy.Item):
    """

    """
    # define the fields for your item here like:
    headline = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    posted_date = scrapy.Field()
    places_mentioned = scrapy.Field()
    text = scrapy.Field()
