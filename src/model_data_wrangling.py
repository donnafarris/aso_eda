# model_data_wrangling.py
from pandas import read_csv, isna, notna
import re
from joblib import dump
from src.data_cleaning import date_formatter, col_renaming_mapper, fix_mixed_data_types, null_handler, check_mixed_types
from src.local import DATA_PATH, ARTIFACTS_PATH

# Column renaming maps for each dataset
col_dicts = [
    {
        '#JCAT': 'JCAT_number', 'Satcat': 'Sat_catalog', 'Piece': 'object_id',
        'Type': 'sat_type', 'Name': 'object_name', 'PLName': 'payload_name',
        'LDate': 'launch_date', 'Parent': 'parent_object', 'SDate': 'status_date',
        'Primary': 'primary', 'DDate': 'phase_end_date', 'Status': 'status',
        'Dest': 'destination', 'Owner': 'object_owner', 'State': 'object_state',
        'Manufacturer': 'manufacturer', 'Bus': 'bus', 'Motor': 'motor', 'Mass': 'mass',
        'MassFlag': 'mass_flag', 'DryMass': 'dry_mass', 'DryFlag': 'dry_flag',
        'TotMass': 'total_mass', 'TotFlag': 'total_flag', 'Length': 'length',
        'LFlag': 'length_flag', 'Diameter': 'diameter', 'DFlag': 'diameter_flag',
        'Span': 'span', 'SpanFlag': 'span_flag', 'Shape': 'shape', 'ODate': 'orbit_date',
        'Perigee': 'perigee_km', 'PF': 'perigee_flag', 'Apogee': 'apogee_km',
        'AF': 'apogee_flag', 'Inc': 'inclination', 'IF': 'incl_flag', 'OpOrbit': 'oper_orbit',
        'OQUAL': 'orbit_quality', 'AltNames': 'alternate_names'
    },
    {
        '#JCAT': 'JCAT_number', 'Piece': 'object_id', 'Name': 'object_name',
        'LDate': 'launch_date', 'TLast': 'last_time', 'TOp': 'oper_time',
        'TDate': 'end_transmit_date', 'TF': 'time_flag', 'Program': 'program',
        'Plane': 'plane', 'Att': 'attitude', 'Mvr': 'maneuver', 'Class': 'class',
        'Category': 'category', 'UNState': 'owner_state', 'UNReg': 'UN_reg',
        'UNPeriod': 'period_mins', 'UNPerigee': 'perigee_km', 'UNApogee': 'apogee_km',
        'UNInc': 'inclination', 'Result': 'result', 'Control': 'control',
        'Discipline': 'discipline', 'Comment': 'comment'
    },
    {
        'OBJECT_NAME': 'object_name', 'OBJECT_ID': 'object_id', 'NORAD_CAT_ID': 'norad_cat_id',
        'OBJECT_TYPE': 'object_type', 'OPS_STATUS_CODE': 'ops_status_code', 'OWNER': 'owner_state',
        'LAUNCH_DATE': 'launch_date', 'LAUNCH_SITE': 'launch_site', 'DECAY_DATE': 'decay_date',
        'PERIOD': 'period_mins', 'INCLINATION': 'inclination', 'APOGEE': 'apogee_km',
        'PERIGEE': 'perigee_km', 'RCS': 'rcs_value', 'DATA_STATUS_CODE': 'data_status',
        'ORBIT_CENTER': 'orbit_center', 'ORBIT_TYPE': 'orbit_type'
    }
]


def load_dataframe(datapath, filename):
    """
    Load a DataFrame from a CSV file.

    Args:
        datapath (str): The directory path containing the CSV file.
        filename (str): The name of the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    return read_csv(f'{datapath}{filename}', low_memory=False)


def apply_cleaning_steps(df, col_rename_map):
    """
    Apply cleaning steps to a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be cleaned.
        col_rename_map (list[dict]): The column renaming maps.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df = col_renaming_mapper(df, col_rename_map)
    df = date_formatter(df, df.columns)
    df = fix_mixed_data_types(df)
    df = null_handler(df)
    df = df.replace({'?': 'Unknown', 'UNK': 'Unknown', 'Unk': 'Unknown'})
    return df


def piece_number_to_letter(piece_number):
    """
    Convert piece number to corresponding letter(s) in base 24 system (omitting I and O).

    Args:
        piece_number (int): The piece number to convert.

    Returns:
        str: The corresponding letter(s).
    """
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    result = ""
    while piece_number > 0:
        piece_number -= 1
        result = letters[piece_number % 24] + result
        piece_number //= 24
    return result


def get_harvard_designation_number(harvard_designation):
    """
    Get the number corresponding to a Harvard designation.

    Args:
        harvard_designation (str): The Harvard designation.

    Returns:
        int: The corresponding number.
    """
    harvard_designation_order = {
        1: 'ALP', 2: 'BET', 3: 'GAM', 4: 'DEL', 5: 'EPS', 6: 'ZET', 7: 'ETA', 8: 'THE', 9: 'IOT', 10: 'KAP',
        11: 'LAM', 12: 'MU', 13: 'NU', 14: 'XI', 15: 'OMI', 16: 'PI', 17: 'RHO', 18: 'SIG', 19: 'TAU', 20: 'UPS',
        21: 'PHI', 22: 'CHI', 23: 'PSI', 24: 'OME', 25: 'A ALP', 26: 'A BET', 27: 'A GAM', 28: 'A DEL', 29: 'A EPS', 30: 'A ZET',
        31: 'A ETA', 32: 'A THE', 33: 'A IOT', 34: 'A KAP', 35: 'A LAM', 36: 'A MU', 37: 'A NU', 38: 'A XI', 39: 'A OMI', 40: 'A PI',
        41: 'A RHO', 42: 'A SIG', 43: 'A TAU', 44: 'A UPS', 45: 'A PHI', 46: 'A CHI', 47: 'A PSI', 48: 'A OME', 49: 'B ALP', 50: 'B BET',
        51: 'B GAM', 52: 'B DEL', 53: 'B EPS', 54: 'B ZET', 55: 'B ETA', 56: 'B THE', 57: 'B IOT', 58: 'B KAP', 59: 'B LAM', 60: 'B MU',
        61: 'B NU', 62: 'B XI', 63: 'B OMI', 64: 'B PI', 65: 'B RHO', 66: 'B SIG', 67: 'B TAU', 68: 'B UPS', 69: 'B PHI', 70: 'B CHI',
        71: 'B PSI', 72: 'B OME'
    }
    return {v: k for k, v in harvard_designation_order.items()}.get(harvard_designation)


def convert_to_launch_order_format(object_id):
    """
    Convert piece ID in Harvard designation format to launch order format.

    Args:
        object_id (str): The object ID to convert.

    Returns:
        str: The converted object ID.
    """
    if re.match(r'^\d{4}-\d{3}[A-Z]+$', object_id):
        return object_id
    parts = object_id.split()
    year = parts[0]
    harvard_designation = None
    piece_number = 1

    if len(parts) == 2:
        harvard_designation = parts[1]
    elif len(parts) == 3:
        harvard_designation = parts[1] if parts[2].isdigit(
        ) else f"{parts[1]} {parts[2]}"
        piece_number = int(parts[2]) if parts[2].isdigit() else 1
    elif len(parts) == 4:
        harvard_designation = f"{parts[1]} {parts[2]}"
        piece_number = int(parts[3])

    harvard_number = get_harvard_designation_number(harvard_designation)
    piece_letter = piece_number_to_letter(piece_number)

    if harvard_number is not None and piece_letter is not None:
        return f"{year}-{harvard_number:03d}{piece_letter}"
    return object_id


def fill_object_type(row):
    """
    Fill missing 'object_type' values based on 'sat_type' values.

    Args:
        row (pd.Series): The DataFrame row.

    Returns:
        str: The filled 'object_type' value.
    """
    if isna(row['object_type']) and notna(row['sat_type']):
        if row['sat_type'].startswith('P'):
            return 'PAY'
        elif row['sat_type'].startswith('D') or row['sat_type'].startswith('C'):
            return 'DEB'
        elif row['sat_type'].startswith('R'):
            return 'R/B'
    return row['object_type']


def clean_dataframe(df, columns_to_clean):
    """
    Clean specific columns in a DataFrame by removing square brackets and trailing question marks.

    Args:
        df (pd.DataFrame): The DataFrame to clean.
        columns_to_clean (list[str]): The columns to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    def remove_square_brackets(value):
        return value.replace('[', '').replace(']', '') if isinstance(value, str) else value

    def remove_trailing_question_mark(value):
        return value[:-1] if isinstance(value, str) and value.endswith('?') else value

    for col in columns_to_clean:
        df[col] = df[col].apply(remove_square_brackets)

    df = df.applymap(remove_trailing_question_mark)
    return df


def filter_columns(df):
    """
    Filter out columns with uniform values or nearly uniform values.

    Args:
        df (pd.DataFrame): The DataFrame to filter.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    drop_columns = [col for col in df.columns if len(df[col].value_counts()) == 1 or (
        len(df[col].value_counts()) == 2 and 1 in df[col].value_counts().values)]
    return df.drop(columns=drop_columns)


# Load data into a dictionary of DataFrames
df_dict = {filename.split('.')[0].split('_')[0]: load_dataframe(
    DATA_PATH, filename) for filename in ['satcat.csv', 'psatcat.csv', 'celestrak_satcat.csv']}

# Apply data cleaning steps to each DataFrame in the dictionary
for key in df_dict:
    df_dict[key] = apply_cleaning_steps(df_dict[key], col_dicts)

# Assign cleaned DataFrames to variables
satcat_df, psatcat_df, celestrak_df = df_dict['satcat'], df_dict['psatcat'], df_dict['celestrak']

# Convert 'object_id' column in SATCAT and PSATCAT DataFrames to launch order format
satcat_df['object_id'] = satcat_df['object_id'].apply(
    convert_to_launch_order_format)
psatcat_df['object_id'] = psatcat_df['object_id'].apply(
    convert_to_launch_order_format)

# Set 'object_id' as the index for merging
for df in df_dict.values():
    df.set_index('object_id', inplace=True)

# Combine DataFrames with preference order: SATCAT, PSATCAT, CELESTRAK
combined_df = satcat_df.combine_first(psatcat_df).combine_first(celestrak_df)

# Update 'object_name' column in combined DataFrame with preferred column from CELESTRAK DataFrame
combined_df['object_name'] = celestrak_df['object_name'].combine_first(
    combined_df['object_name'])

# Reset the index to bring 'object_id' back as a column
combined_df.reset_index(inplace=True)

# Split 'oper_orbit' column into 'oper_orbit' and 'inc_category'
split_oper_orbit = combined_df['oper_orbit'].str.split('/', expand=True)
combined_df['oper_orbit'], combined_df['inc_category'] = split_oper_orbit[0], split_oper_orbit[1]

# Fill NaN values in 'object_type' column based on 'sat_type' column
combined_df['object_type'] = combined_df.apply(fill_object_type, axis=1)

# Clean specific columns in the combined DataFrame
combined_df = clean_dataframe(combined_df, ['object_state', 'owner_state'])

# Reorder columns in the combined DataFrame
columns_list = [
    'JCAT_number', 'Sat_catalog', 'object_id', 'object_type', 'object_name',
    'payload_name', 'launch_date', 'orbit_date', 'oper_time', 'oper_orbit',
    'parent_object', 'program', 'object_state', 'object_owner',
    'owner_state', 'manufacturer', 'launch_site', 'control', 'destination',
    'class', 'category', 'discipline', 'comment', 'status', 'status_date',
    'data_status', 'phase_end_date', 'end_transmit_date', 'last_time',
    'time_flag', 'decay_date', 'result', 'bus', 'motor', 'mass', 'dry_mass',
    'total_mass', 'length', 'diameter', 'span', 'shape', 'rcs_value',
    'orbit_center', 'orbit_type', 'perigee_km', 'apogee_km', 'inclination',
    'inc_category', 'period_mins', 'plane', 'maneuver', 'alternate_names',
    'UN_reg'
]
combined_df = combined_df.reindex(columns=columns_list)

# Replace '?' and 'UNK' with 'Unknown' in the entire DataFrame
combined_df.replace({'?': 'Unknown', 'UNK': 'Unknown',
                    'Unk': 'Unknown'}, inplace=True)

# Filter out columns with uniform values or nearly uniform values
combined_df = filter_columns(combined_df)

# Drop rows where the 'status' column is null
combined_df.dropna(subset=['status'], inplace=True)

# Define the mapping for converting status values
status_conversion = {'AR': 'R', 'AO': 'O', 'ATT': 'DK',
                     'TFR': 'DK', 'GRP': 'DK', 'OX': 'ERR', 'C': 'E'}

# Convert status values in the 'status' column
combined_df['status'] = combined_df['status'].replace(status_conversion)

# Define the list of statuses to drop
statuses_to_drop = ['DSO', 'DSA', 'REL', 'EVA DP']

# Drop rows where the 'status' column has values to be removed
combined_df = combined_df[~combined_df['status'].isin(statuses_to_drop)]

# Save the cleaned and combined DataFrame to a CSV file
combined_df.to_csv(f'{DATA_PATH}combined_df.csv', index=False)

# Save the cleaned and combined DataFrame to a .joblib file
dump(combined_df, f'{ARTIFACTS_PATH}combined_df.joblib')
