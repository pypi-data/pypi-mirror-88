import quickscreen.analysis.datafill as dfl
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


class Lm(dfl.DataEdit):
    """
    A class for easy linear regression functions on a pandas dataframe
    """

    def __init__(self, data):
        """
        description

        Parameters
        ----------
        data : pandas.Dataframe
            the data to have linear regression functions applied to

        Returns
        -------
        None

        Examples
        --------
        >>> Lm(pd.Dataframe(data))
        """
        try:
            dfl.DataEdit.__init__(self, data)
            assert isinstance(self.data, pd.core.frame.DataFrame) 
        except AssertionError:
            print("Not a Pandas data frame.")

    def single_linear(self, predictor, estimator):
        """
        fits a single linear regression with the estimator as the independant variable
        and predictor as the dependant variable fits the model to these columns
        then predicts y values using the estimator values

        Parameters
        ----------
        predictor : int or string
            the column name or index for the y values in the regression
        estimator : int or string
            the column name or index for the x values in the regression

        Returns
        -------
        prediction : ndarray
            predictions of the estimator from the model fit on the estimator data

        Examples
        --------
        >>> lm = Lm(df)
        >>> slr = lm.single_linear("column_name_for_y", "column_name_for_x")
        """

        try:
            assert (isinstance(estimator, int) or estimator in self.data)
            x = self.data[estimator].to_numpy().reshape(-1,1)
        except AssertionError:
            print("Please enter an integer or the name of a column for the estimator")
            return
            
        try:
            assert (isinstance(predictor, int) or predictor in self.data)
            y = self.data[predictor].to_numpy().reshape(-1,1)
        except AssertionError:
            print("Please enter an integer or the name of a column for the predictor")
            return
            
        l_regressor = LinearRegression()
        l_regressor.fit(x,y)
        prediction = l_regressor.predict(x)
        return prediction

    def single_linear_plot(self, predictor, estimator):
        """
        creates a plot of the predictor vs estimator
        and includes the best fit line
        and displays the plot

        Parameters
        ----------
        predictor : int or string
            the column name or index for the y values in the regression
        estimator : int or string
            the column name or index for the x values in the regression

        Returns
        -------
        None

        Examples
        --------
        >>> lm = Lm(df)
        >>> lm.single_linear_plot("column_name_for_y", "column_name_for_x")
        """
        try:
            assert (isinstance(estimator, int) or estimator in self.data)
            x = self.data[estimator].to_numpy().reshape(-1,1)
        except AssertionError:
            print("Please enter an integer or the name of a column for the estimator")
            return
            
        try:
            assert (isinstance(predictor, int) or predictor in self.data)
            y = self.data[predictor].to_numpy().reshape(-1,1)
        except AssertionError:
            print("Please enter an integer or the name of a column for the predictor")
            return

        prediction = self.single_linear(predictor, estimator)

        plt.scatter(x, y)
        plt.plot(x, prediction, color='red')
        plt.title("Linear Regression")
        plt.xlabel(estimator)
        plt.ylabel(predictor)

        return plt.show()

    def single_linear_eqn(self, predictor, estimator):
        """
        fits a single linear regression model and displays the
        equation of the best fit line

        Parameters
        ----------
        predictor : int or string
            the column name or index for the y values in the regression
        estimator : int or string
            the column name or index for the x values in the regression

        Returns
        -------
        None

        Examples
        --------
        >>> lm = Lm(df)
        >>> lm.single_linear_eqn("horsepower", "enginesize")
        """
        try:
            assert (isinstance(estimator, int) or estimator in self.data)
            x = self.data[estimator].to_numpy().reshape(-1,1)
        except AssertionError:
            print("Please enter an integer or the name of a column for the estimator")
            return

        try:
            assert (isinstance(predictor, int) or predictor in self.data)
            y = self.data[predictor].to_numpy().reshape(-1,1)
        except AssertionError:
            print("Please enter an integer or the name of a column for the predictor")
            return

        l_regressor = LinearRegression()
        l_regressor.fit(x,y)

        coef = round(float(l_regressor.coef_),2)
        intercept = round(float(l_regressor.intercept_),2)
        return ({"Coefficient":coef,"Intercept":intercept})
        


