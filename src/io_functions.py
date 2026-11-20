'''
    Helper functions
'''
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm
from statsmodels.stats import power


def bootstrap_ci(a: pd.Series, b: pd.Series, perms = 1000):
    '''Performs a simple bootstrap and return the ci'''
    all_vals = np.concatenate([a, b])
    n_a = len(a)
    obs_diff = b.mean() - a.mean()

    perm_diffs = np.empty(perms)
    for i in range(perms):
        perm = np.random.permutation(all_vals)
        perm_a, perm_b = perm[:n_a], perm[n_a:]
        perm_diffs[i] = perm_b.mean() - perm_a.mean()
    
    p_perm = np.mean(np.abs(perm_diffs) >= abs(obs_diff))
    ci_low_perm, ci_high_perm = np.percentile(perm_diffs, [2.5, 97.5])
    return obs_diff, p_perm, (ci_low_perm, ci_high_perm)

def calc_power(a: pd.Series, b: pd.Series, alt: str = "two-sided") -> float:
    '''
    Calculates and returns power with a 5% significance level
    
    a: The first data sample

    b: The second data sample

    alt: What calculation to use, two-sided, larger, or smaller
    '''

    n_a, n_b = len(a), len(b)
    pooled_sd = np.sqrt(
        ((n_a - 1) * a.std()**2 + (n_b - 1) * b.std()**2) / (n_a + n_b - 2)
    )

    effect = (a.mean() - b.mean()) / pooled_sd

    return power.TTestIndPower().power(effect, n_a, 0.05, (n_b / n_a), alternative=alt) # type: ignore


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Takes in the medical data and refactors
    the entries into more managable data types
    '''
    output = df.copy()
    output = output.drop_duplicates()
    output["sex"] = output["sex"].map({"M": "Male", "F": "Female"})
    output["smoker"] = output["smoker"].map({"No": 0, "Yes": 1})
    return output

def compose_values(s: pd.Series) -> str:
    '''
    Returns mean, median, min and max values for the provided DataFrame

    s: Column to get values from

    column_name: String to be printed before the composed values
    '''

    return f"Mean: {mean(s)}, Median: {median(s)}, Min: {s.min()}, Max: {s.max()}"

def get_truncated_normal(
    mean: float,
    sd: float,
    low: float,
    high: float
):
    '''
    Returns an object that can generate a random normal distributed number within 2 points
    
    mean: The mean value of data

    sd: Standard deviation

    low: Lowest value of the data

    high: Highest value of the data
    '''
    return stats.truncnorm(
        (low - mean) / sd, (high - mean) / sd, loc = mean, scale = sd
    )

def mean(s: pd.Series):
    '''Returns the mean values of the supplied Series'''
    return round(s.mean(), 2)

def median(s: pd.Series):
    '''Returns the median values of the supplied Series'''
    return round(s.median(), 2)

def minmax(s: pd.Series) -> tuple:
    '''Returns the min and the max value of the supplied Series as a tuple'''
    return (s.min(), s.max())

def normal_mean_ci(a: pd.Series, b: pd.Series) -> tuple:
    '''Calculates the confidence interval between 2 samples using normal approximation'''
    difference = a.mean() - b.mean()
    se = np.sqrt(a.var() / len(a) + b.var() / len(b))
    z = norm.ppf(0.975)

    return (difference - z * se, difference + z * se)

def print_composed_values(df: pd.DataFrame):
    print(f"Age: {compose_values(df["age"])}")
    print(f"Height: {compose_values(df["height"])}")
    print(f"Weight: {compose_values(df["weight"])}")
    print(f"Blood Pressure: {compose_values(df["systolic_bp"])}")
    print(f"Cholesterol: {compose_values(df["cholesterol"])}")

def t_test(s1: pd.Series, s2: pd.Series, equal_var=True, alternative="two-sided") -> tuple:
    '''
    Perform a t-test comparison between 2 Series
    returns a tuple with the t_score and p_value as floats
    '''
    t_score, p_value = stats.ttest_ind(s1, s2, equal_var=equal_var, alternative=alternative)

    return (t_score, p_value)
