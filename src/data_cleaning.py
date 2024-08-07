# data_cleaning.py
import pandas as pd
from joblib import dump


def date_formatter(dataframe, columns):
    """
    Formats specified columns in a DataFrame to datetime format.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the columns to be formatted.
        columns (list[str]): A list of column names to be checked and formatted.

    Returns:
        pd.DataFrame: The DataFrame with the specified columns formatted as datetime.
    """
    for c in columns:
        if 'datetime' not in str(type(dataframe.dtypes[c])).lower():
            if ('_jd' in c.lower()) or ('julian_date' in c.lower()):
                dataframe[c] = pd.to_datetime(
                    dataframe[c], unit='D', origin='julian')
            elif (('date' in c.lower()) or ('time' in c.lower())) and 'flag' not in c.lower():
                dataframe[c] = pd.to_datetime(
                    dataframe[c], errors='coerce', format='mixed')
    return dataframe


def col_renaming_mapper(df, col_name_dict_list=None):
    """
    Renames the columns of a DataFrame based on a list of column name mapping dictionaries.

    Args:
        df (pd.DataFrame): The DataFrame whose columns are to be renamed.
        col_name_dict_list (list[dict], optional): A list of dictionaries where each dictionary maps old column names to new column names.

    Returns:
        pd.DataFrame: The DataFrame with renamed columns, if a matching dictionary is found; otherwise, the original DataFrame.
    """
    if col_name_dict_list is None:
        return df
    for d in col_name_dict_list:
        if all(col in df.columns for col in d.keys()):
            df = df.rename(columns=d)
            return df
    return df


def col_val_mapper(df, old_col_name, new_col_name, col_val_dict_list=None):
    """
    Maps the values of a specified column to new values based on a list of dictionaries.

    Args:
        df (pd.DataFrame): The DataFrame containing the column to be mapped.
        old_col_name (str): The name of the column whose values are to be mapped.
        new_col_name (str): The name of the new column to be created with mapped values.
        col_val_dict_list (list[dict], optional): A list of dictionaries for mapping the column values.

    Returns:
        pd.DataFrame: The DataFrame with the new column containing mapped values.
    """
    if col_val_dict_list is None:
        return df
    for d in col_val_dict_list:
        if old_col_name in df.columns and set(df[old_col_name].unique()) == set(d.keys()):
            df[new_col_name] = df[old_col_name].map(d)
            return df
    return df


def check_mixed_types(df):
    """
    Identifies columns in a DataFrame that contain mixed data types.

    Args:
        df (pd.DataFrame): The DataFrame to be checked for mixed data types.

    Returns:
        dict: A dictionary where keys are column names and values are arrays of unique data types found in those columns.
    """
    mixed_types_columns = {}
    timestamp_type = pd._libs.tslibs.timestamps.Timestamp
    nat_type = pd._libs.tslibs.nattype.NaTType
    for col in df.columns:
        types = df[col].map(type).unique().tolist()
        if len(types) > 1:
            if not (len(types) == 2 and timestamp_type in types and nat_type in types):
                mixed_types_columns[col] = types
    return mixed_types_columns


def fix_mixed_data_types(df):
    """
    Fixes mixed data types in the DataFrame columns where the types are 'str' and 'float'.

    Args:
        df (pd.DataFrame): The DataFrame to be fixed.

    Returns:
        pd.DataFrame: The DataFrame with fixed data types.
    """
    mixed_types = check_mixed_types(df)

    def try_convert(value):
        try:
            return float(value)
        except ValueError:
            return value

    for col, types in mixed_types.items():
        if str in types and float in types:
            df[col] = df[col].apply(lambda x: try_convert(
                x) if isinstance(x, str) else x)
            if len(df[col].map(type).unique()) > 1:
                df[col] = df[col].astype(str)
    return df


def null_handler(df):
    """
    Handles null values and duplicates in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be processed.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    df = df.replace(['-', 'nan'], [None, None])
    df = df.dropna(axis=1, how='all')
    df = df.dropna(thresh=df.shape[1] - 2, axis=0)
    df = df.drop_duplicates()
    return df


def df_dict_formatter(dataframe_dict, col_name_dict_list=None):
    """
    Formats a dictionary of DataFrames by renaming columns and converting date-related columns.

    Args:
        dataframe_dict (dict): A dictionary where keys are identifiers and values are DataFrames to be formatted.
        col_name_dict_list (list[dict], optional): A list of dictionaries where each dictionary maps old column names to new column names.

    Returns:
        dict: The dictionary with formatted DataFrames.
    """
    for k, df in dataframe_dict.items():
        dataframe_dict[k] = col_renaming_mapper(df, col_name_dict_list)
        dataframe_dict[k] = date_formatter(df, df.columns)
        dataframe_dict[k] = fix_mixed_data_types(df)
        dataframe_dict[k] = null_handler(df)
    return dataframe_dict


def identify_numeric_outliers(df):
    """
    Identifies outliers in numeric columns of a DataFrame using the IQR method.

    Args:
        df (pd.DataFrame): The DataFrame to be processed.

    Returns:
        pd.DataFrame: A DataFrame containing rows with outliers, including the column name and outlier value.
    """
    numeric_cols = df.select_dtypes(include='number').columns
    outliers_list = []
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].copy()
        if not outliers.empty:
            outliers['outlier_column'] = col
            outliers['outlier_value'] = df[col]
            outliers_list.append(outliers)
    if outliers_list:
        outliers_combined = pd.concat(outliers_list).drop_duplicates()
    else:
        outliers_combined = pd.DataFrame()
    return outliers_combined


def generate_data_artifacts(filepath, data):
    """
    Save data to a file using the joblib serialization format.

    Args:
        filepath (str): The path to the file where the data will be saved.
        data (any): The data to be serialized and saved.

    Returns:
        None
    """
    with open(filepath, 'wb') as f:
        dump(data, f, protocol=5)
