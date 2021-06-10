#News Crawler

Scrapy crawler to scrap news articles. 

# Prerequisites

- MongoDB

The crawler uses MongoDB to store crawled data. I have used  https://www.mongodb.com/cloud/atlas
to store the documents. You can create it for free. 

Change the following piece of code in settings.py with your mongo db credentials: 

```
MONGODB_USERNAME = urllib.parse.quote_plus(
    get_ssm_parameter('MONGODB_USERNAME'))
MONGODB_PWD = urllib.parse.quote_plus(
    get_ssm_parameter('MONGODB_PWD',
                      with_decryption=True))
MONGODB_URI = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PWD}" \
              f"@news-scraper.a2rmv.mongodb.net/" \
              f"ary_news?retryWrites=true&w=majority"
MONGODB_DB = 'ary_news'
```

if you are running the application locally, 
comment out the following code in settings.py

```
ssm = boto3.client('ssm', region_name='us-east-1')


def get_ssm_parameter(name: str, with_decryption=False) -> str:
    try:
        response = ssm.get_parameter(
            Name=name,
            WithDecryption=with_decryption)
        parameter = response['Parameter']['Value']
    except ClientError as error:
        print(error.response['Error']['Code'])
        raise
    return parameter
```

# Usage

To run locally: 
1. ```export PYTHONPATH=/path/to/news_crawler```
2. ```make run-local ds=YYYY-MM-dd```

If ```make run-local ds=YYY-MM-DD``` fails, do ```make clean``` and then run it again.
The results will be crawledcl and posted to mongodb database
