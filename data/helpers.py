from constants import *
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Tuple

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

# Model train helpers
def convert_data_to_matrix(data: pd.DataFrame,  weight_casualty: bool = False) -> np.array:
    """
    Convert csv data to matrix of shape(D, US_NUM_STATES),
    where D = latest date - earliest date + 1 in days.

    Params
    ------
    data: pd.DataFrame
        input data from csv file

    Returns
    -------
    np.array:
        matrix of shape (D, US_NUM_STATES)
    """

    data = data.sort_values('Date')

    # If data type is pd.Timestamp, convert to datetime.datetime
    if isinstance(data.iloc[0, 0], pd.Timestamp):
        data['Date'] = data['Date'].to_pydatetime()

    start_date, end_date = data.iloc[0, 0], data.iloc[-1, 0]
    D = (end_date - start_date).days + 1

    ret_matrix = np.zeros((D, US_NUM_STATES), dtype = int)
    
    for i in range(len(data)):
        idx = (data.iloc[i, 0] - start_date).days
        state = get_state_code(data.iloc[i, 1])
        weight = 1
        if weight_casualty:
            weight = data.iloc[i, 3] if data.iloc[i, 3] > 0 else 0
        ret_matrix[idx, state] += weight

    return ret_matrix

# def get_x_y(data: pd.DataFrame, matrix: np.array, lookback: int = 10) -> Tuple[np.array, np.array]:
