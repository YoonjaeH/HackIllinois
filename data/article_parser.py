import requests
from requests.api import options
# from newsapi import NewsApiClient
from pynytimes import NYTAPI
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath('.'))
from credentials import NYT_KEY, NYT_SECRET
from constants import KEY_WORDS
from datetime import datetime

nyt = NYTAPI(NYT_KEY, parse_dates=True)

search = nyt.article_search(
    query = KEY_WORDS[0],
    dates = {
        'begin' : datetime(2017, 1, 1),
        'end'   : datetime(2021, 4, 1)
    },
    options = {
        "sources" : [
            "New York Times",
            "AP",
            "Reuters",
            "International Herald Tribune"
        ]
    }
)

print(search)

# '''
#  publishedAt -> timestamp
# '''
# if __name__ == '__main__':
#     api = NewsApiClient(api_key=API_KEY)
#     #news = api.get_everything(q='discrimination', language='en')
#     for key in KEY_WORDS:
#         news = api.get_everything(q=key, language='en')
#         print(len(news['articles']))
#         break


