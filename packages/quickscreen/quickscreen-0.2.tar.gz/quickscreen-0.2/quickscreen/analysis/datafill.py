#linear.py
import pandas as pd

class PandaError(Exception):

    def __init__(self):
        pass 

    def __str__(self):
        return ("Not a Pandas data frame")

class ColumnId(Exception):

    def __init__(self, type):
        self.type = type

    def __str__(self):
        if self.type==1:
            return ("This column number is out of range.")
        elif self.type==0:
            return ("This column name is not in the data frame.")



class DataEdit:
    """
    A class for easy dataframe manipulation
    """

    def __init__(self, data):
        """
        Initializes data edit class

        Parameters
        ----------
        data : pandas.Dataframe
            the pandas dataframe to be manipulated

        Returns
        -------
        None

        Examples
        --------
        >>> DataEdit(pd.Dataframe(data))
        """
        self.data = data
        try:
            if type(self.data)!=pd.DataFrame:
                raise PandaError()
        except PandaError as p:
            print(p)
        #assert isinstance(self.data, pd.core.frame.DataFrame), print("Not a Pandas data frame.")


    def display(self):
        """
        Getter function for data

        Parameters
        ----------
        None

        Returns
        -------
        pandas.Dataframe
            class's data
        """
        return self.data



    def columntype(self, column):
        """
        Gets the data type for the column specified by index or by nane

        Parameters
        ----------
        column : int or string
            int - column index, string - column name

        Returns
        -------
        numpy.dtype
            dtype of column
        """
        try:
            c=None

            if (column not in self.data):
                if isinstance(column, int)==True:
                    if column>=len(self.data.columns):
                        c=1
                else:
                    c=0

            if c in (0,1):
                raise ColumnId(c)

        except ColumnId as p:
            print(p)
            return

        return self.data.dtypes[column]

    def __add__(self, other):
        """
        appends one dataframe to another

        Parameters
        ----------
        other : pandas.Dataframe
            the dataframe to add to the original

        Returns
        -------
        pandas.Dataframe
            the two dataframes appended

        Examples
        --------
        >>> DataEdit(df1) + df2
        """
        try:
            if type(other)!=pd.DataFrame:
                raise PandaError()
        except PandaError as p:
            print(p)
            return
        
        return DataEdit(self.data.append(other, ignore_index=True))
            
    def __sub__(self, other):
        """
        removes the insersection of the two dataframes

        Parameters
        ----------
        other : pandas.Dataframe
            the dataframe to intersect with the original

        Returns
        -------
        pandas.Dataframe
            original dataframe with interseciton with other removed
        
        Examples
        --------
        >>> difference = DataEdit(df1) - df2
        """
        try:
            if type(other)!=pd.DataFrame:
                raise PandaError()
        except PandaError as p:
            print(p)
            return
        try:
            common = self.data.merge(other, indicator='i', how='outer').query('i=="left_only"').drop('i',1)
        except:
            common = self.data
        return DataEdit(common)



    def rm_duplicates(self):
        """
        removes duplicate rows from DataEdit object's data

        Parameters
        ----------
        None

        Returns
        -------
        DataEdit instance
            with the same data as the original object, but with duplicate rows removed
        
        Examples
        --------
        >>> DataEdit(df).rm_duplicates()
        """
        
        return DataEdit(self.data.drop_duplicates())

        
    def rm_nan(self):
        """
        Removes rows that have na for values

        Parameters
        ----------
        None

        Returns
        -------
        DataEdit instance
            with the same data as the original object,
            but with rows comintaining na removed
        
        Examples
        --------
        >>> DataEdit(df1).rm_nan()
        """

        return DataEdit(self.data.dropna(axis=0))  


    def quick_clean(self):
        """
        Removes rows that have na for values and rows that are duplicates

        Parameters
        ----------
        None

        Returns
        -------
        DataEdit instance
            with the same data as the original object,
            but with rows comintaining na removed,
            and duplicate rows removed
        
        Examples
        --------
        >>> DataEdit(df1).quick_clean()
        """

        return DataEdit(self.data.drop_duplicates().dropna(axis=0))