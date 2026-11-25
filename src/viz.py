'''
    Methods for visualising data
'''
from dataclasses import dataclass

import numpy as np
import pandas as pd
from matplotlib.axes import Axes


@dataclass
class GraphTexts:
    '''
    Common texts for graphs

    title: The title of the graph

    x_label: The label of the x axis

    y_label: The label of the y axis
    '''

    title: str = ""
    x_label: str = ""
    y_label: str = ""


def _set_common_values(ax: Axes, texts: GraphTexts | None = None, grid: str = ""):
    '''
    Sets values that all graphs share, such as titles and labels
	'''

    if texts:
        if texts.title:
            ax.set_title(texts.title)
        if texts.x_label:
            ax.set_xlabel(texts.x_label)
        if texts.y_label:
            ax.set_ylabel(texts.y_label)

    if grid == "both" or grid == "x" or grid == "y":
        ax.grid(axis=grid)


def add_normal_fit(ax: Axes, s: pd.Series, color: str | None = None, label: str = "", bins = 0):
    '''
    Adds a normal distribution to a plot
    
    ax: Plot you want to modify

    s: Series to show the normal distribution of

    color: Optional color

    label: Optional label

    bins: If plotted to a histogram bins scales the plot
    '''
    values = s.to_numpy()
    mean = values.mean()
    std = values.std(ddof=1)

    x = np.linspace(values.min(), values.max(), 300)
    pdf = np.exp(-0.5 * ((x - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))

    if bins:
        bin_edges = np.histogram_bin_edges(values, bins)
        pdf *= len(values) * np.diff(bin_edges).mean()

    ax.plot(x, pdf, color=color, linewidth=2, label=f"{label} normal fit")


def box(ax: Axes, s: pd.Series, tick_labels: list[str], texts: GraphTexts | None = None):
    '''
    Creates a box plot

    ax: The subplot you want to modify

    s: Series of values to display as boxes

    tick_labels: List of strings for group names, indices must match Series indices
    '''

    ax.boxplot(s, notch=True, tick_labels=tick_labels, bootstrap=5000)
    _set_common_values(ax, texts, "y")


def grouped_bar(
    ax: Axes,
    height: list[list],
    labels: list[str],
    tick_labels: list[str],
    texts: GraphTexts | None = None
):
    '''
    Creates a grouped bar chart

    ax: The subplot you want to modify

    height: Set of values to group in the bar chart, list entires must match tick_labels

    tick_labels: The groups to sort the bars into

    texts: Optional title and axis labels
    '''

    ax.grouped_bar(height, labels=labels, tick_labels=tick_labels)
    ax.legend()
    _set_common_values(ax, texts, "y")


def hist(ax: Axes, s: pd.Series, bins: int, texts: GraphTexts | None = None, labels: str | list[str] | None = None, color: str | None = None):
    '''
    Creates a histogram with the supplied values

    ax: The subplot that you want to modify

    s: Series of the values you want to display

    bins: The number of bars you want the data to be displayed in

    texts: Optional title and axis labels

    labels: Optional label names for legend

    color: Optional color string
    '''

    ax.hist(s, bins=bins, color=color, label=labels, alpha=0.9)
    _set_common_values(ax, texts, "y")


def scatter(ax: Axes,
            x: pd.Series,
            y: pd.Series,
            texts: GraphTexts | None = None,
            dot_color: str | None = None,
            trend_color: str | None = None,
            label: str | None = None,
            trend_label: str | None = None):
    '''
    Creates a scatter plot with the supplied values

    ax: The plot you want to modify

    x: Series with the x-values to display

    y: Series with the y-values to display

    texts: Optional title and axis labels

    trend_color: String for the color of the trend line. If not defined no trend line is displayed

    label: String label for legend

    trend_label: String label of trend line for legend
    '''

    ax.scatter(x, y, c=dot_color, alpha=0.8, label=label)
    if trend_color:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x.to_numpy()), c=trend_color, label=trend_label)
    _set_common_values(ax, texts, "both")
