import datetime
from sys import platform

import pandas as pd
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt


class Plotter:
    """
    Generic plotting class used in the grapher module
    """

    def __init__(self, data, plot_title=None, label_names=None):
        """
        Initializes plotting class with an optional plot title and label

        Parameters
        ----------
        data : pandas.DataFrame
            the Pandas Dataframe to be plotted
        plot_title : str, optional (default = None)
            the plot title
        label_names : str tuple, optional (default = None)
            the x-axis and y-axis titles (x-axis is position [0], y-axis is position [1])

        Returns
        -------
        None

        Examples
        --------
        >>> Plotter(pd.DataFrame(data), "Name of Plot", ("Name of X-axis", "Name of Y-axis"))
        """
        self.data = data
        self.plot_title = plot_title
        self.label_names = label_names

    def add_title(self, title):
        """
        Adds plot title to Plotter class

        Parameters
        ----------
        title : str
            the plot title
        """
        self.plot_title = title

    def add_label_names(self, x_label, y_label):
        """
        Adds axis labels to Plotter class

        Parameters
        ----------
        x_label : str
            x-axis label
        y_label : str
            y-axis label
        """
        self.label_names = (x_label, y_label)

    def show_plot(self):
        """
        Function to show plot with title and axis labels

        Parameters
        ----------
        None
        """
        if self.label_names:
            plt.xlabel(self.label_names[0])
            plt.ylabel(self.label_names[1])
        if self.plot_title:
            plt.title(self.plot_title)
        plt.show()

    def save_plot(self, file_name=None):
        """
        Function to save plot as jpg, only on MacOS
        Saves to current working directory

        Parameters
        ----------
        file_name : str, optional (default = None)
            filename for plot
            will use date and time as default filename

        Returns
        -------
        None
            Saves plot as .jpg

        Examples
        --------
        >>> working_plot = Plotter(pd.DataFrame(data))
        >>> working_plot.save_plot(file_name="final_plot")
        """
        # doesnt work on windows
        # untested on linux
        if platform != "darwin":
            raise Exception("Can only save plot on MacOS")

        if self.label_names:
            plt.xlabel(self.label_names[0])
            plt.ylabel(self.label_names[1])
        if self.plot_title:
            plt.title(self.plot_title)
        if file_name is None:
            x = datetime.datetime.now()
            str_date = str(x.date()) +"_"+ str(x.time())
            file_name = type(self).__name__ + "_" + str_date
            print(file_name)
        plt.savefig(file_name + ".jpg")
