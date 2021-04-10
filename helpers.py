from constants import *

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
