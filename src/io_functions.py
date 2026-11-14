'''
    Helper functions
'''

import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes in the medical data and refactors
    the entries into more managable data types
    '''
    output = df.copy()
    output["sex"] = output["sex"].map({"M": "Male", "F": "Female"})
    output["smoker"] = output["smoker"].map({"No": 0, "Yes": 1})
    return output

def compose_values(s: pd.Series, column_name: str):
    '''
    Prints mean, median, min and max values for the provided DataFrame

    s: Column to get values from

    column_name: String to be printed before the composed values
    '''
    print(f"{column_name}:  Mean: {mean(s)}, Median: {median(s)}, Min: {s.min()}, Max: {s.max()}")

def mean(s: pd.Series):
    '''Returns the mean values of the supplied Series'''
    return round(s.mean(), 2)

def median(s: pd.Series):
    '''Returns the median values of the supplied Series'''
    return round(s.median(), 2)

def minmax(s: pd.Series) -> tuple:
    '''Returns the min and the max value of the supplied Series as a tuple'''
    return (s.min(), s.max())
