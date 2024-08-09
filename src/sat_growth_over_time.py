# sat_growth_over_time.py
from pandas import to_datetime, merge, concat
from src.helpers import get_line_plot, display_plot


def get_launch_decay_orbit_over_time(df):
    """
    Analyzes satellite launch, decay, and on-orbit counts over time.

    Args:
        df (pd.DataFrame): DataFrame containing satellite data with 'launch_date' and 'decay_date' columns.

    Returns:
        pd.DataFrame: A DataFrame with cumulative counts of launches, decays, and satellites on orbit over time.
    """
    df['launch_year'] = to_datetime(df['launch_date']).dt.year
    df['launch_month_year'] = to_datetime(
        df['launch_date']).dt.to_period('M').astype(str)
    launches_over_time = df.groupby(
        ['launch_month_year']).size().reset_index(name='launch_count')
    launches_over_time['launches'] = launches_over_time['launch_count'].cumsum()

    df['decay_month_year'] = to_datetime(
        df['decay_date']).dt.to_period('M').astype(str)
    decays_over_time = df.dropna(subset=['decay_date']).groupby(
        ['decay_month_year']).size().reset_index(name='decay_count')
    decays_over_time['decayed_sats'] = decays_over_time['decay_count'].cumsum()

    merged_df = merge(launches_over_time, decays_over_time,
                      on='month_year', how='outer').fillna(0)
    merged_df['on_orbit'] = (
        merged_df['launch_count'] - merged_df['decay_count']).cumsum()
    return merged_df


def get_sat_growth_over_time_plot(display_data):
    """
    Generate a line plot showing satellite growth over time.

    Args:
        display_data (pd.DataFrame): The data to be plotted, containing columns 'month_year', 'on_orbit', 'launches', and 'decayed_sats'.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly Figure object representing the satellite growth over time plot.
    """
    fig = get_line_plot(
        display_data=display_data,
        x_col='month_year',
        y_col=['on_orbit', 'launches', 'decayed_sats'],
        labels={'value': 'Count', 'month_year': 'Year'},
        title='Satellite Growth Over Time',
        color_sequence=['#2c57c9', '#8d50d0', '#c95574']
    )
    return fig


def display_sat_growth_over_time_plot(display_data, png_path=None, html_path=None):
    """
    Display and optionally save the satellite growth over time plot.

    Args:
        display_data (pd.DataFrame): The data to be plotted.
        png_path (str, optional): The file path to save the plot as a PNG image. Default is None.
        html_path (str, optional): The file path to save the plot as an HTML file. Default is None.

    Returns:
        None
    """
    fig = get_sat_growth_over_time_plot(display_data)
    display_plot(fig, png_path, html_path)


def get_starlink_vs_other_launches(df):
    """
    Compares Starlink launches to other satellite launches over time.

    Args:
        df (pd.DataFrame): DataFrame containing satellite data with 'satellite_name', 'launch_year', and 'launch_month_year' columns.

    Returns:
        pd.DataFrame: A DataFrame with cumulative launch counts for Starlink and other satellites, categorized by type.
    """
    starlink_satcat_df = df[(df['satellite_name'].str.contains(
        'STARLINK', na=False)) & (df['launch_year'] > 2019)]
    starlink_launches = starlink_satcat_df.groupby(
        'launch_month_year').size().cumsum().reset_index(name='launches')
    starlink_launches['type'] = 'Starlink'

    other_satcat_df = df[(~df['satellite_name'].str.contains(
        'STARLINK', na=False)) & (df['launch_year'] > 2019)]
    other_launches = other_satcat_df.groupby(
        'launch_month_year').size().cumsum().reset_index(name='launches')
    other_launches['type'] = 'Other'

    combined_launches = concat([starlink_launches, other_launches])
    return combined_launches


def get_starlink_vs_all_other_sats_plot(display_data):
    """
    Generate a line plot comparing Starlink launches versus all other satellite launches over time.

    Args:
        display_data (pd.DataFrame): The data to be plotted, containing columns 'launch_month_year', 'launches', and 'type'.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly Figure object representing the comparison of Starlink and all other satellite launches over time.
    """
    fig = get_line_plot(
        display_data=display_data,
        x_col='launch_month_year',
        y_col='launches',
        labels={'launch_month_year': 'Year', 'launches': 'Number of Launches'},
        title='Number of Starlink vs All Other Satellite Launches',
        color_sequence=['#2c57c9', '#c95574'],
        color_col='type'
    )
    return fig


def display_starlink_vs_all_other_sats_plot(display_data, png_path=None, html_path=None):
    """
    Display and optionally save the plot comparing Starlink launches versus all other satellite launches.

    Args:
        display_data (pd.DataFrame): The data to be plotted.
        png_path (str, optional): The file path to save the plot as a PNG image. Default is None.
        html_path (str, optional): The file path to save the plot as an HTML file. Default is None.

    Returns:
        None
    """
    fig = get_starlink_vs_all_other_sats_plot(display_data)
    display_plot(fig, png_path, html_path)
