import pandas as pd
import os


def tsv_to_csv(data_path):
    """
    Converts all .tsv files in the specified directory to .csv files.

    This function reads each .tsv file in the provided directory, converts it to a .csv file, and handles any trailing tab characters by using an exception block.

    Args:
        data_path (str): The directory path containing .tsv files to be converted.

    Handles:
        FileNotFoundError: If the provided directory path does not exist.
        FileExistsError: If the provided file name already exists.
        pd.errors.ParserError: If a parsing error occurs during the reading of a .tsv file.
    """
    for file in os.listdir(data_path):
        if file.endswith('.tsv'):
            try:
                try:
                    df = pd.read_csv(f'{data_path}{file}',
                                     sep='\t').drop(0, axis=0)
                    df.to_csv(
                        f'{data_path}{file[:-4]}.csv', index=False, mode='x')
                except pd.errors.ParserError:
                    with open(f'{data_path}{file}', 'r') as inf, open(f'{data_path}{file[:-4]}.csv', 'w') as of:
                        for line in inf:
                            if line[-2] != '\t':
                                of.write(
                                    ','.join([s.replace(",", ":").strip() for s in line.split('\t')]) + '\n')
                            else:
                                of.write(
                                    ','.join([s.replace(",", ":").strip() for s in line[:-2].split('\t')]) + '\n')
                    df = pd.read_csv(
                        f'{data_path}{file[:-4]}.csv').drop(0, axis=0)
                    df.to_csv(
                        f'{data_path}{file[:-4]}.csv', index=False, mode='x')
            except FileExistsError:
                continue


def csv_to_df_dict(data_path):
    """
    Converts all CSV files in a specified directory to a dictionary of DataFrames.

    This function reads each CSV file in the provided directory, converts it to a pandas DataFrame, 
    and stores it in a dictionary where the keys are the filenames (without the .csv extension) 
    appended with '_df', and the values are the corresponding DataFrames.

    Args:
        data_path (str): The directory path containing CSV files to be converted.

    Returns:
        dict: A dictionary with keys as modified filenames and values as pandas DataFrames.
    """
    df_dict = {}
    for file in os.listdir(data_path):
        if file.endswith('.csv'):
            df = pd.read_csv(f'{data_path}{file[:-4]}.csv', delimiter=',')
            df_dict[f'{file[:-4]}_df'] = df
    return df_dict
