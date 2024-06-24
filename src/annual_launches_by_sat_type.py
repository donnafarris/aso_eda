from data_cleaning import col_val_mapper
from constants import ALL_VAL_RENAME_DICTS
from helpers import display_bar_plot


def get_launch_count_by_sat_class(psatcat_df):
    """
    Calculates the annual count of satellite launches categorized by satellite class.

    This function adds a 'launch_year' column to the DataFrame based on the 'launch_date' column,
    maps satellite class values to human-readable names using a predefined dictionary,
    and groups the data by 'launch_year' and 'class' to count the number of launches each year for each class.

    Args:
        psatcat_df (pd.DataFrame): The DataFrame containing satellite data with 'launch_date' and 'class' columns.

    Returns:
        pd.DataFrame: A DataFrame with the annual count of satellite launches categorized by satellite class.
                      The DataFrame has columns: 'launch_year', 'class', and 'launch_count'.
    """
    # Drop rows missing critical data
    psatcat_df = psatcat_df.dropna(subset=['class', 'launch_date']).copy()
    # Add launch_year column
    psatcat_df['launch_year'] = psatcat_df['launch_date'].dt.year
    # Rename class values to human readable names
    psatcat_df = col_val_mapper(psatcat_df, 'class',
                                'class', ALL_VAL_RENAME_DICTS)
    launch_count_by_sat_class = psatcat_df.groupby(
        ['launch_year', 'class']).size().reset_index(name='launch_count')
    return launch_count_by_sat_class


def display_launch_count_by_sat_class_plot(psatcat_df, png_path=None, html_path=None):
    """
    Displays and optionally saves a bar plot of the annual number of satellite launches categorized by satellite class.

    This function generates a bar plot using the Plotly library to visualize the annual number of satellite launches
    by satellite class. It utilizes the `get_launch_count_by_sat_class` function to obtain the data, grouping by launch year
    and satellite class. Optionally, it saves the plot as a PNG and/or HTML file if paths are providedl

    Args:
        psatcat_df (pd.DataFrame): The DataFrame containing satellite data with 'launch_date' and 'class' columns.
        png_path (str, optional): The file path to save the plot as a PNG image. If None, the plot is not saved as a PNG.
        html_path (str, optional): The file path to save the plot as an HTML file. If None, the plot is not saved as an HTML file.

    Returns:
        None: The function displays the plot and optionally saves it as a PNG and/or HTML file.
    """
    display_bar_plot(display_data=get_launch_count_by_sat_class(psatcat_df),
                     color_col_name='class', title='Annual Number of Launches by Satellite Type', png_path=png_path, html_path=html_path)
