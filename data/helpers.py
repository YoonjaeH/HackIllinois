import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from constants import *
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Tuple
from newspaper import Article

# Data processing/parsing helpers
def get_state_code(data: str) -> int:
    """
    Convert web-scraped state data to state code.

    Params
    ------
    data: str
        state name (i.e. 'Illinois', 'IL') to be converted.

    Returns
    -------
    int:
        converted state code
    """

    data_lower = data.lower()
    if not data_lower in US_STATE_CODE_DICT:
        return -1
    return US_STATE_CODE_DICT[data_lower]

def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    """
    Converts Quarter_start_date to datetime
    Remove underscore from state and converts to lower case state

    Params
    ------
    data: pd.dataFrame
        dataframe to be preprocessed

    Returns
    -------
    data: pd.dataFrame
        processed dataframe
    """
    # Remove period
    data['Quarter_start_date'] = data['Quarter_start_date'].str.replace('.', '')
    # Convert to date_time
    data['Quarter_start_date'] = pd.to_datetime(data['Quarter_start_date'], format='%Y%m%d')

    # Replace underscore with a space
    data['State'] = data['State'].str.replace('_', ' ')
    # Conver to lowercase
    data['State'] = data['State'].str.lower()

    return data
# Model train helpers
def convert_data_to_matrix(data: pd.DataFrame,  weight_casualty: bool = False) -> np.array:
    """
    Convert csv data to matrix of shape(D, US_NUM_STATES),
    where D = latest date - earliest date + 1 in days.

    Params
    ------
    data: pd.DataFrame
        input data from csv file

    weight_casualty: bool
        boolean option to weight matrix by casualty of the event or not. Default is False.

    Returns
    -------
    np.array:
        matrix of shape (D, US_NUM_STATES)
    """
    data = preprocess(data)
    data = data.sort_values('Quarter_start_date')
    # If data type is pd.Timestamp, convert to datetime.datetime
    if isinstance(data.iloc[0, 0], pd.Timestamp):
        data['Quarter_start_date'] = data['Quarter_start_date'].dt.to_pydatetime()
    start_date, end_date = data.iloc[0, 0], data.iloc[-1, 0]
    #print(start_date, end_date)
    D = (end_date - start_date).days + 1
    #print('d = ', D)
    ret_matrix = np.zeros((D, US_NUM_STATES), dtype = int)
    for i in range(len(data)):
        idx = (data.iloc[i, 0] - start_date).days
        state = get_state_code(data.iloc[i, 1])
        weight = 1
        if weight_casualty:
            weight = data.iloc[i, 2] if data.iloc[i, 2] > 0 else 0
        ret_matrix[idx, state] += weight

    return ret_matrix

# Data collecting helpers
def get_article_location(text: str) -> str:
    """
    From the input article text, get most frequent occurence state in state code.

    Params
    ------
    text: str
        article text to find the state

    Returns
    -------
    str:
        state name. Returns None if no state was detected.
    """

    text = text.lower()
    state_freq_array = np.zeros(US_NUM_STATES, dtype = int)
    for i in range(50):
        count = 0
        count += text.count(US_STATE_NAMES[i])
        count += text.count(US_STATE_POSTAL_CODES[i])
        count += text.count(US_STATE_ABBR[i])
        state_freq_array[i] = count

    if np.max(state_freq_array) == 0: 
        return None

    return US_STATE_NAMES[np.argmax(state_freq_array)]

def get_article_text(url: str) -> str:
    """
    From the article url, returns the text of the article.html

    Params
    ------
    url: str
        article url string to retrieve the text

    Returns
    -------
    str:
        article text
    """
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def is_valid_article(date : datetime, state : str, date_start : datetime, date_end : datetime) -> bool:
    """
    Determines if the metadata retrived from the article is valid.

    Params
    ------
    date: datetime.datetime
        Published datetime of the article

    state: str
        detected state of the incident in the article

    date_start: datetime.datetime
        article search beginning timeframe

    date_end: datetime.datetime
        article search ending timeframe
    """

    return isinstance(state, str) and date >= date_start and date <= date_end




if __name__== '__main__':
    df = pd.read_csv('./data_format.csv')
    ret = convert_data_to_matrix(df, True)
    np.savetxt('data.csv', ret, delimiter=',')
# def get_x_y(data: pd.DataFrame, matrix: np.array, lookback: int = 10) -> Tuple[np.array, np.array]:
