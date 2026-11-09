from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import pandas as pd

def _set_common_values(ax: Axes,
                       title: str = "",
					   x_label: str = "",
                       y_label: str = "",
					   grid: str = ""):
	ax.set_title(title)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	if grid == "both" or grid == "x" or grid == "y":
		ax.grid(axis = grid)

def box(ax: Axes,
        df: pd.DataFrame,
		title: str = "",
		x_label: str = "",
        y_label: str = ""):
	ax.box(df)
	_set_common_values(ax, title, x_label, y_label, "y")

def hist(ax: Axes,
         df: pd.DataFrame,
		 bins: int,
		 title: str = "",
		 x_label: str = "",
         y_label: str = ""):
	ax.hist(df, bins = bins)
	_set_common_values(ax, title, x_label, y_label, "y")

def line(ax: Axes,
         df: pd.DataFrame,
		 title: str = "",
		 x_label: str = "",
		 y_label: str = ""):
	ax.plot(df)
	_set_common_values(ax, title, x_label, y_label, "both")

def scatter(ax: Axes,
            x: pd.DataFrame,
            y: pd.DataFrame,
			title: str = "",
			x_label: str = "",
			y_label: str = ""):
	ax.scatter(x, y)
	_set_common_values(ax, title, x_label, y_label, "both")