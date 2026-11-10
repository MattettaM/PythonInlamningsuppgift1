'''
    Methods for visualising data
'''

from dataclasses import dataclass

from matplotlib.axes import Axes
import numpy as np
import pandas as pd

@dataclass
class GraphTexts:
    '''
    Common texts for graphs

    title: The title of the graph

    x_label: The label of the x axis

    y_label: The label of the y axis
    '''

    title: str
    x_label: str
    y_label: str


def _set_common_values(ax: Axes, texts: GraphTexts | None, grid: str = ""):
    '''
    Sets values that all graphs share, such as titles and labels
	'''

    ax.set_title(texts.title)
    ax.set_xlabel(texts.x_label)
    ax.set_ylabel(texts.y_label)
    if grid == "both" or grid == "x" or grid == "y":
        ax.grid(axis=grid)


def box(ax: Axes, df: pd.DataFrame, texts: GraphTexts | None):
    '''
    Creates a box plot

    Not done
    '''

    ax.box(df)
    _set_common_values(ax, texts, "y")


def grouped_bar(ax: Axes, df: pd.DataFrame, texts: GraphTexts | None):
    '''
    Creates a grouped bar chart

    Not done
    '''

    ax.grouped_bar(df)
    ax.legend()
    _set_common_values(ax, texts, "y")


def hist(ax: Axes, df: pd.DataFrame, bins: int, texts: GraphTexts | None):
    '''
    Creates a histogram with the supplied values

    ax: The subplot that you want to modify

    df: DataFrame of the values you want to display

    bins: The number of bars you want the data to be displayed in

    texts: Optional title and axis labels
    '''

    ax.hist(df, bins=bins)
    _set_common_values(ax, texts, "y")


def line(ax: Axes, df: pd.DataFrame, texts: GraphTexts | None):
    '''
    Creates a line graph

    Not done
    '''

    ax.plot(df)
    _set_common_values(ax, texts, "both")


def scatter(ax: Axes, x: pd.DataFrame, y: pd.DataFrame,
            texts: GraphTexts | None, trend: bool = False):
    '''
    Creates a scatter plot with the supplied values

    ax: The plot you want to modify

    x: DataFrame with the x-values to display

    y: DataFrame with the y-values to display

    title: Optional chart title

    x_label: Optional x label

    y_label: Optional y label

    trend: Should a trend line be displayed?
    '''

    ax.scatter(x, y)
    if trend:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), "r")
    _set_common_values(ax, texts, "both")
