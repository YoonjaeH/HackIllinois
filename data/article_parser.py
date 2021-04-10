## API KEY: fa2d8290ba3c4544b316dc90df84b47c
import requests
from newsapi import NewsApiClient

API_KEY='fa2d8290ba3c4544b316dc90df84b47c'
KEY_WORDS=[
'discrimination',
]

'''
 publishedAt -> timestamp
'''
if __name__ == '__main__':
    api = NewsApiClient(api_key=API_KEY)
    #news = api.get_everything(q='discrimination', language='en')
    for key in KEY_WORDS:
        news = api.get_everything(q=key, language='en')
    print((news['totalResults']))
