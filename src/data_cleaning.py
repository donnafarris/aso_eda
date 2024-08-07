import pandas as pd
from joblib import dump


def date_formatter(dataframe, columns: list[str]):
    """
    Formats specified columns in a DataFrame to datetime format.

    This function checks each column in the provided list to determine if it contains date or time information
    and converts it to a datetime format. Columns containing 'date' or 'time' in their name, excluding those with 'flag',
    are converted using pandas' to_datetime with error coercion. Columns with '_jd' in their name are interpreted as Julian dates.

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


def col_renaming_mapper(df, col_name_dict_list: list[dict] = None):
    """
    Renames the columns of a DataFrame based on a list of column name mapping dictionaries.

    This function checks the DataFrame's columns against each dictionary in the provided list.
    If the DataFrame's columns match the keys of any dictionary, it renames the columns according to that dictionary.
    If no matching dictionary is found, the DataFrame remains unchanged.

    Args:
        df (pd.DataFrame): The DataFrame whose columns are to be renamed.
        col_name_dict_list (list[dict], optional): A list of dictionaries where each dictionary maps old column names to new column names.

    Returns:
        pd.DataFrame: The DataFrame with renamed columns, if a matching dictionary is found; otherwise, the original DataFrame.
    """
    if col_name_dict_list == None:
        return df
    for d in col_name_dict_list:
        if (list(df.columns) == list(d.keys())):
            df = df.rename(columns=d)
            return df
        else:
            continue


def col_val_mapper(df, old_col_name, new_col_name, col_val_dict_list: list[dict] = None):
    """
    Maps the values of a specified column to new values based on a list of dictionaries.

    This function checks if the specified column in the DataFrame has the same set of unique values as the keys
    in any of the dictionaries in the provided list. If a match is found, it creates a new column with the mapped values.

    Args:
        df (pd.DataFrame): The DataFrame containing the column to be mapped.
        old_col_name (str): The name of the column whose values are to be mapped.
        new_col_name (str): The name of the new column to be created with mapped values.
        col_val_dict_list (list[dict], optional): A list of dictionaries for mapping the column values.

    Returns:
        pd.DataFrame: The DataFrame with the new column containing mapped values.
    """
    if col_val_dict_list == None:
        return df
    for d in col_val_dict_list:
        if (old_col_name in list(df.columns)) and (list(dict(df[old_col_name].value_counts()).keys()) == list(d.keys())):
            df.loc[:, new_col_name] = df[old_col_name].map(d)
            return df
        else:
            continue


def check_mixed_types(df):
    """
    Identifies columns in a DataFrame that contain mixed data types, excluding columns with only
    Timestamp and NaTType types.

    This function iterates over each column in the DataFrame and checks for the presence of multiple 
    data types within the same column. If a column contains mixed data types, it adds the column 
    name and the types to a dictionary, excluding columns with only Timestamp and NaTType types.

    Args:
        df (pd.DataFrame): The DataFrame to be checked for mixed data types.

    Returns:
        dict: A dictionary where keys are column names and values are arrays of unique data types found in those columns.
    """
    mixed_types_columns = {}
    timestamp_type = pd._libs.tslibs.timestamps.Timestamp
    nat_type = pd._libs.tslibs.nattype.NaTType

    for col in df.columns:
        types = df[col].map(type).unique()
        types = types.tolist()
        if len(types) > 1:
            if (len(types) == 2) and (timestamp_type in types) and (nat_type in types):
                continue
            mixed_types_columns[col] = types

    return mixed_types_columns


def fix_mixed_data_types(df):
    """
    Fixes mixed data types in the DataFrame columns where the types are 'str' and 'float'.

    This function identifies columns with mixed 'str' and 'float' data types and attempts to convert 
    numeric 'str' values to 'float'. If there are non-numeric 'str' values, it converts 'float' values to 'str'.

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
        if len(types) <= 3 and str in types and float in types:
            # Attempt to convert 'str' values to 'float'
            df[col] = df[col].apply(lambda x: try_convert(
                x) if isinstance(x, str) else x)
            # Check if there are still mixed types
            if len(df[col].map(type).unique()) > 1:
                # If still mixed, convert 'float' values to 'str'
                df[col] = df[col].apply(lambda x: str(
                    x) if isinstance(x, float) else x)

    return df


def null_handler(df):
    """
    Handles null values and duplicates in a DataFrame.

    This function performs the following operations on the input DataFrame:
    1. Converts all '-' values to nulls.
    2. Drops columns where all values are null.
    3. Removes duplicate rows.

    Args:
        df (pd.DataFrame): The DataFrame to be processed.

    Returns:
        pd.DataFrame: The processed DataFrame with '-' values converted to nulls, 
                      columns with all nulls dropped, and duplicate rows removed.
    """
    df = df.replace('-', None)  # Convert '-' to nulls
    df = df.replace('nan', None)  # Convert 'nan' to nulls

    # Drop columns where all values are null
    df = df.dropna(axis=1, how='all')
    df = df.dropna(thresh=df.shape[1]-(df.shape[1] - 2), axis=0)
    df = df.drop_duplicates()
    return df


def df_dict_formatter(dataframe_dict: dict, col_name_dict_list: list[dict] = None):
    """
    Formats a dictionary of DataFrames by renaming columns and converting date-related columns.

    This function iterates over each DataFrame in the provided dictionary, applies column renaming 
    using predefined dictionaries, and formats date-related columns to datetime format.

    Args:
        dataframe_dict (dict): A dictionary where keys are identifiers and values are DataFrames to be formatted.
        col_name_dict_list (list[dict], optional): A list of dictionaries where each dictionary maps old column names to new column names.


    Returns:
        dict: The dictionary with formatted DataFrames.
    """
    for k in list(dataframe_dict.keys()):
        dataframe_dict[k] = col_renaming_mapper(
            dataframe_dict[k], col_name_dict_list)
        dataframe_dict[k] = date_formatter(
            dataframe_dict[k], dataframe_dict[k].columns)
        dataframe_dict[k] = fix_mixed_data_types(dataframe_dict[k])
        dataframe_dict[k] = null_handler(dataframe_dict[k])
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
        # Combine all outliers into a single DataFrame
        outliers_combined = pd.concat(outliers_list).drop_duplicates()
    else:
        # Return an empty DataFrame if no outliers were found
        outliers_combined = pd.DataFrame()

    return outliers_combined


def generate_data_artifacts(filepath, data):
    """
    Save data to a file using the joblib serialization format.

    Parameters:
    filepath (str): The path to the file where the data will be saved.
    data (any): The data to be serialized and saved. This can be any Python object supported by the joblib module.

    Returns:
    None
    """
    with open(filepath, 'wb') as f:
        dump(data, f, protocol=5)
