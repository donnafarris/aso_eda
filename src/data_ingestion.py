# data_ingestion.py
import pandas as pd
import os


def tsv_to_csv(data_path):
    """
    Converts all .tsv files in the specified directory to .csv files.

    Args:
        data_path (str): The directory path containing .tsv files to be converted.
    """
    for file in os.listdir(data_path):
        if file.endswith('.tsv'):
            try:
                df = pd.read_csv(f'{data_path}{file}',
                                 sep='\t').drop(0, axis=0)
                df.to_csv(f'{data_path}{file[:-4]}.csv', index=False, mode='x')
            except pd.errors.ParserError:
                with open(f'{data_path}{file}', 'r') as inf, open(f'{data_path}{file[:-4]}.csv', 'w') as of:
                    for line in inf:
                        if line[-2] != '\t':
                            of.write(
                                ','.join([s.replace(",", ":").strip() for s in line.split('\t')]) + '\n')
                        else:
                            of.write(','.join([s.replace(",", ":").strip()
                                     for s in line[:-2].split('\t')]) + '\n')
                df = pd.read_csv(f'{data_path}{file[:-4]}.csv').drop(0, axis=0)
                df.to_csv(f'{data_path}{file[:-4]}.csv', index=False, mode='x')
            except FileExistsError:
                continue


def csv_to_df_dict(data_path):
    """
    Converts all CSV files in a specified directory to a dictionary of DataFrames.

    Args:
        data_path (str): The directory path containing CSV files to be converted.

    Returns:
        dict: A dictionary with keys as modified filenames and values as pandas DataFrames.
    """
    df_dict = {}
    for file in os.listdir(data_path):
        if file.endswith('.csv'):
            df = pd.read_csv(f'{data_path}{file}', delimiter=',')
            df_dict[f'{file[:-4]}_df'] = df
    return df_dict
