import requests
from newsapi import NewsApiClient
import credentials

KEY_WORDS=[
'discrimination',
'hate',
'hatred',
'racism',
'asian hatred',
'racial',
'minorities',
'asian',
'crime'
]


'''
 publishedAt -> timestamp
'''
if __name__ == '__main__':
    api = NewsApiClient(api_key=credentials.API_KEY)
    #news = api.get_everything(q='discrimination', language='en')
    for key in KEY_WORDS:
        news = api.get_everything(q=key, language='en')
        print((news['totalResults']))
