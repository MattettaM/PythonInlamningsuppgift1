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
    output["smoker"] = output["smoker"].map({"No": 0, "Yes": 1})
    return output

def mean(df: pd.DataFrame):
    '''Returns the mean values of the supplied DataFrame'''
    return df.mean()

def median(df: pd.DataFrame):
    '''Returns the median values of the supplied DataFrame'''
    return df.median()
