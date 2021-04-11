Please follow the format of the 'data_format.csv' in the current directory.

Data type of each columns should follow as below:

- Date: pd.Timestamp or datetime.datetime
- State: str
- Occurences: int

Notes:
- Data does not have to be sorted
- If Date cannot be retrieved or parsed, its data should be left as None