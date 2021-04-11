import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from constants import *
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import torch
from torch.utils.data import TensorDataset, DataLoader, Dataset
from sklearn.model_selection import train_test_split
from typing import Tuple
from newspaper import Article


# Convert Training Data to PyTorch DataLoader
def get_dataloader(x_data,y_data,batch_size=32):
    # Convert to Torch Tensors
    x = torch.from_numpy(x_data).float()
    # y = torch.from_numpy(y_data).long()
    y = torch.from_numpy(y_data).float()

    # TensorDataset & Loader
    dataset = TensorDataset(x,y)
    loader  = DataLoader(dataset,batch_size=batch_size,shuffle=True,drop_last=True)
    return loader

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
def convert_data_to_matrix(data: pd.DataFrame,  weight_casualty: bool = False, **kwargs) -> Tuple[np.array, np.array]:
    """
    Convert csv data to matrix of shape(D, US_NUM_STATES),
    where D = latest date - earliest date + 1 in days.

    Params
    ------
    data: pd.DataFrame
        input data from csv file

    weight_casualty: bool
        boolean option to weight matrix by casualty of the event or not. Default is False.

    **kwargs: keyword arguments
        group_data: bool
            boolean option to group the data by certain period of days or not
        group_days: int
            if group_data, number of days to group the data by

    Returns
    -------
    np.array:
        matrix of shape (D, US_NUM_STATES)

    np.array:
        1D array of shape (D, ). Contains date that each rows of ret_matrix represents.
    """
    # data = preprocess(data)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values('Date')

    # If data type is pd.Timestamp, convert to datetime.datetime
    if isinstance(data.iloc[0, 0], pd.Timestamp):
        data['Date'] = data['Date'].dt.to_pydatetime()

    start_date, end_date = data.iloc[0, 0], data.iloc[-1, 0]
    D = (end_date - start_date).days + 1
    days_delta = 1

    # If kwargs group_data and group_days are True and valid
    if 'group_data' in kwargs.keys() and kwargs['group_data'] and \
        'group_days' in kwargs.keys() and kwargs['group_days'] > 0:
        days_delta = kwargs['group_days']
        D = int(np.ceil(D / days_delta))

    ret_matrix = np.zeros((D, US_NUM_STATES), dtype = int)
    date_array = np.array([start_date + timedelta(days = i * days_delta) for i in range(D)])
    for i in range(len(data)):
        idx = (data.iloc[i, 0] - start_date).days // days_delta
        state = get_state_code(data.iloc[i, 1])
        weight = 1
        if weight_casualty:
            weight = data.iloc[i, 2] if data.iloc[i, 2] > 0 else 0
        ret_matrix[idx, state] += weight

    return ret_matrix, date_array

def get_x_y(matrix: np.array, lookback: int = 10) -> Tuple[np.array, np.array]:
    '''
    Generate features and label sets from data matrix

    Params
    ------
    matrix: np.array
        Data matrix containing daily report of occurence
    lookback: Integer
        Number of previous days to consider in deciding output

    Returns
    -------
    (x,y): Tuple(np.array, np.array)
        Feature and label set given lookback date
    '''
    x,y=[],[]
    N = len(matrix)
    for i in range(N-lookback):
        x.append(matrix[i:i+lookback])
        y.append(matrix[i+lookback])

    return np.array(x),np.array(y)

def split_data(x: np.array, y: np.array, test_size=0.25, random_state=32, batch=32):
    range_ = range(len(y))
    train_idx,_,_,_ = train_test_split(range_, y,test_size=test_size,random_state=random_state)
    train_idx,test_idx,_,_ = train_test_split(train_idx, y[train_idx],test_size=test_size,random_state=random_state)

    train_data = get_dataloader(x[train_idx],y[train_idx], batch)
    test_data = get_dataloader(x[test_idx],y[test_idx], batch)

    return train_data, test_data

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
        count = text.count(US_STATE_NAMES[i])
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

    Returns
    -------
    bool:
        boolean value determining whether the article is valid or not
    """
    
    return isinstance(state, str) and date >= date_start and date <= date_end

def format_datetime(dt: datetime) -> datetime:
    """
    Helper function to format datetime to truncate time.

    Params
    ------
    dt: datetime.datetime
        datetime object to truncate time

    Returns
    -------
    datetime.datetime:
        time-truncated datetime object

    """
    return datetime(dt.year, dt.month, dt.day)

# Model train helpers
def get_pred(outs):
    return torch.round(outs)

def calc_accuracy(pred, y):
    y_sum = np.abs(torch.sum(y))
    diff_sum = np.abs(torch.sum(torch.sub(pred, y)))
    return 1 if y_sum == 0 else 1 - diff_sum / y_sum

def calc_strict_accuracy(pred, y):
    total = y.flatten().size(0)
    correct = (pred.flatten() == y.flatten()).sum().item()
    return correct / total

if __name__== '__main__':
    df = pd.read_csv('./data_format.csv')
    ret = convert_data_to_matrix(df, True)
    x,y = get_x_y(ret, 40)
    train,test = split_data(x,y)
