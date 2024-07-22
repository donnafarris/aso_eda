from data_cleaning import col_val_mapper
from constants import ALL_VAL_RENAME_DICTS
from helpers import get_bar_plot, display_plot


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


def get_launch_count_by_sat_class_plot(display_data):
    """
    Generate a bar plot showing the annual number of launches categorized by satellite type.

    Parameters:
    display_data (DataFrame): The data to be plotted, containing columns for launch year, launch count, and satellite class.

    Returns:
    Figure: A Plotly Figure object representing the annual number of launches by satellite type.
    """
    fig = get_bar_plot(
        display_data=display_data,
        color_col_name='class',
        title='Annual Number of Launches by Satellite Type'
    )
    return fig


def display_launch_count_by_sat_class_plot(display_data, png_path=None, html_path=None):
    """
    Display and optionally save the bar plot showing the annual number of launches by satellite type.

    Parameters:
    display_data (DataFrame): The data to be plotted.
    png_path (str, optional): The file path to save the plot as a PNG image. Default is None.
    html_path (str, optional): The file path to save the plot as an HTML file. Default is None.

    Returns:
    None
    """
    fig = get_launch_count_by_sat_class_plot(display_data)
    display_plot(fig, png_path, html_path)
