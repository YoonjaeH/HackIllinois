from data.helpers import get_article_location, get_article_text, is_valid_article
import requests
# from newsapi import NewsApiClient
from pynytimes import NYTAPI
import sys
import os
sys.path.append(os.path.abspath('.'))
from credentials import NYT_KEY
from constants import *
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm


nyt = NYTAPI(NYT_KEY, parse_dates=True)

date_start = datetime(2017, 1, 1)
date_end = datetime.now()
delta = timedelta(days = 7)

date_list, state_list = [], []

pbar = tqdm(total = (date_end - date_start).days // 7 + 1)

while date_start < date_end:
    date_delta_added = min(date_start + delta, date_end)
    for keyword in KEY_WORDS:
        search = nyt.article_search(
            query = keyword,
            dates = {
                'begin' : date_start,
                'end'   : date_delta_added
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
        for i in range(len(search)):
            article_time, article_url = search[i]['pub_date'], search[i]['web_url']
            article_text = get_article_text(article_url)
            article_state = get_article_location(article_text)
            if is_valid_article(article_time, article_state, date_start, date_delta_added):
                article_time = datetime(article_time)
                date_list.append(article_time)
                state_list.append(article_state)

    date_start = date_delta_added
    pbar.update(1)

pbar.close()

occurence = [1] * len(date_list)
article_df = pd.DataFrame({'Date' : date_list, 'State' : state_list, 'Occurence' : occurence})
article_df.to_csv('./data/data_from_news.csv', index=False)
    

