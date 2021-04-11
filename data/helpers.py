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

def data_split_sliding_window(x: np.array, y: np.array, lookback: int) -> Tuple[np.array, np.array]:
    x_data = []
    y_data = []
    N = len(x)
    for index in range(N-lookback):
        x_data.append(x[index: index + lookback])
        y_data.append(y[index: index + lookback])
    return np.array(x_data), np.array(y_data)

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
    return x,y


if __name__== '__main__':
    df = pd.read_csv('./data_format.csv')
    ret = convert_data_to_matrix(df, True)
    test_arr = np.zeros((10,50))
    x,y = get_x_y(test_arr, 8)
