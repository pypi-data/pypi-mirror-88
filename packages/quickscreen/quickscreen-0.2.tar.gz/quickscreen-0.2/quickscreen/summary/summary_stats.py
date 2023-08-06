# summary_stats.py
import pandas as pd

from quickscreen.summary.summary_classes import *


def missing_summary(df, type="columns"):
    """
    Outputs the count and percent of null values in a Pandas Dataframe for each column or row.

    Parameters
    ----------
    df : pandas.DataFrame
        Pandas Dataframe to be viewed
    type : str, optional {"columns", "rows"}

    Returns
    -------
    pandas.Dataframe
        The total null values and the percent of null values.

    Examples
    --------
    >>> missing_summary(pd.DataFrame(df), "rows")
    """
    try:
        data = Missing(df, type)
        if not hasattr(data, "df"):
            raise Exception
    except:
        print("Can not complete function")
        return

    df_out = {
        "count_missing": data.count_missing,
        "percent_missing": data.percent_missing,
    }

    return pd.concat(df_out, axis=1)


def stats_summary(df, type="columns"):
    """
    Outputs the max, min, and mean of a Pandas Dataframe for each column or row.

    Parameters
    ----------
    df : pandas.DataFrame
        Pandas Dataframe to be viewed
    type : str, optional {"columns", "rows"}

    Returns
    -------
    pandas.Dataframe
        The maximum, minimum, and mean values.

    Examples
    --------
    >>> stats_summary(pd.DataFrame(df), "rows")
    """
    try:
        data = Stats(df, type)
        if not hasattr(data, "df"):
            raise Exception
    except:
        print("Can not complete function")
        return

    df_out = {"max": data.sub_max, "min": data.sub_min, "mean": data.sub_mean}

    return pd.concat(df_out, axis=1)


def all_summary(df, type="columns"):
    """
    Outputs the maximum, minimum, mean, null count, and percentage null values of a Pandas Dataframe for each column or row.

    Parameters
    ----------
    df : pandas.DataFrame
        Pandas Dataframe to be viewed
    type : str, optional {"columns", "rows"}

    Returns
    -------
    pandas.Dataframe
        The maximum, minimum, mean, null count, and percentage null values of a Pandas Dataframe for each column or row.

    Examples
    --------
    >>> Df_Info(pd.DataFrame(df), "rows")
    """
    try:
        data1 = stats_summary(df, type)
        if data1 is None:
            raise Exception
    except:
        return

    data2 = missing_summary(df, type)
    return pd.concat([data1, data2], axis=1)


def simple_summary(df):
    """
    Outputs the max, min, and mean values of a Pandas dataframe as well as the row count, columns count, and null count.

    Parameters
    ----------
    df : pandas.DataFrame
        Pandas Dataframe to be viewed


    Returns
    -------
    pandas.Dataframe
        The maximum, minimum, mean, amound of rows and columns, and total null values.

    Examples
    --------
    >>> Df_Info(pd.DataFrame(df), "rows")
    """
    try:
        data = Df_Info(df)
        if not hasattr(data, "df"):
            raise Exception
    except:
        print("Can not complete function")
        return

    output_labels = [
        "df_max",
        "df_min",
        "df_mean",
        "row_count",
        "column_count",
        "total_missing",
    ]
    output_values = [
        data.total_max(),
        data.total_min(),
        data.total_mean(),
        data.rows,
        data.columns,
        data.total_missing(),
    ]
    return pd.DataFrame({"values": output_values}, index=output_labels)
