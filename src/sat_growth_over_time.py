import pandas as pd
from helpers import display_line_plot


def get_launch_decay_orbit_over_time(df):
    """
    Analyzes satellite launch, decay, and on-orbit counts over time.

    This function processes a DataFrame containing satellite data to calculate the total number of launches,
    the number of decayed satellites, and the number of satellites remaining in orbit over time. The results
    are returned as a combined DataFrame with cumulative counts for each month-year period.

    Args:
        df (pd.DataFrame): DataFrame containing satellite data with 'launch_date' and 'decay_date' columns.

    Returns:
        pd.DataFrame: A DataFrame with cumulative counts of launches, decays, and satellites on orbit over time.
    """
    # Get the total number of launches over time
    df['launch_year'] = df['launch_date'].dt.year
    df['launch_month_year'] = df['launch_date'].dt.to_period(
        'M').astype(str)
    launches_over_time = df.groupby(['launch_month_year']).size()
    launches_over_time = launches_over_time.reset_index()
    launches_over_time = launches_over_time.rename(
        columns={'launch_month_year': 'month_year', 0: 'launch_count'})
    launches_over_time['launches'] = launches_over_time['launch_count'].cumsum()

    # Get the number of satellites decayed over time
    df['decay_month_year'] = df['decay_date'].dt.to_period(
        'M').astype(str)
    decays_over_time = df.dropna(subset='decay_date').groupby([
        'decay_month_year']).size()
    decays_over_time = decays_over_time.reset_index()
    decays_over_time = decays_over_time.rename(
        columns={'decay_month_year': 'month_year', 0: 'decay_count'})
    decays_over_time['decayed_sats'] = decays_over_time['decay_count'].cumsum()

    # Create a combined dataframe to work with
    merged_df = pd.merge(launches_over_time, decays_over_time,
                         on='month_year', how='outer').fillna(0)
    merged_df['on_orbit'] = (
        merged_df['launch_count'] - merged_df['decay_count']).cumsum()
    on_orbit = merged_df[['month_year', 'on_orbit']]
    return merged_df


def display_sat_growth_over_time_plot(df, png_path=None, html_path=None):
    """
    Displays a line plot of satellite growth over time and optionally saves the plot.

    This function generates and displays a line plot using Plotly Express, showing the cumulative number of satellites
    on orbit, launches, and decayed satellites over time. The data is processed by the `get_launch_decay_orbit_over_time`
    function. Optionally, it saves the plot as a PNG and/or HTML file if paths are provided.

    Args:
        df (pd.DataFrame): DataFrame containing satellite data with 'launch_date' and 'decay_date' columns.
        png_path (str, optional): The file path to save the plot as a PNG image. If None, the plot is not saved as a PNG.
        html_path (str, optional): The file path to save the plot as an HTML file. If None, the plot is not saved as an HTML file.

    Returns:
        None: The function displays the plot and optionally saves it as a PNG and/or HTML file.
    """
    display_line_plot(display_data=get_launch_decay_orbit_over_time(df), x_col='month_year', y_col=['on_orbit', 'launches', 'decayed_sats'], labels={
        'value': 'Count',
        'month_year': 'Year'
    }, title='Satellite Growth Over Time', color_sequence=['#2c57c9', '#8d50d0', '#c95574'], png_path=png_path, html_path=html_path)


def get_starlink_vs_other_launches(df):
    """
    Compares Starlink launches to other satellite launches over time.

    This function filters the DataFrame to separate Starlink satellite launches from other satellite launches
    for the years after 2019, as that is when Starlink satellites began launching. 
    It calculates the cumulative number of launches per month-year for both Starlink 
    and other satellites and combines the results into a single DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing satellite data with 'satellite_name', 'launch_year', and 'launch_month_year' columns.

    Returns:
        pd.DataFrame: A DataFrame with cumulative launch counts for Starlink and other satellites, categorized by type.
    """
    # Get Starlink launches per year
    starlink_satcat_df = df[(df['satellite_name'].str.contains(
        'STARLINK', na=False)) & (df['launch_year'] > 2019)]
    starlink_launches = starlink_satcat_df.groupby(
        'launch_month_year').size().cumsum().reset_index(name='launches')
    starlink_launches['type'] = 'Starlink'

    # Get other launches per year
    other_satcat_df = df[(~df['satellite_name'].str.contains(
        'STARLINK', na=False)) & (df['launch_year'] > 2019)]
    other_launches = other_satcat_df.groupby(
        'launch_month_year').size().cumsum().reset_index(name='launches')
    other_launches['type'] = 'Other'

    # Combine
    combined_launches = pd.concat([starlink_launches, other_launches])

    return combined_launches


def display_starlink_vs_all_other_sats_plot(df, png_path=None, html_path=None):
    """
    Displays a line plot comparing the number of Starlink launches to all other satellite launches over time and optionally saves the plot.

    This function generates and displays a line plot using Plotly Express, showing the cumulative number of Starlink launches 
    versus other satellite launches from the years after 2019. The data is processed by the `get_starlink_vs_other_launches` 
    function. Optionally, it saves the plot as a PNG and/or HTML file if paths are provided.

    Args:
        df (pd.DataFrame): DataFrame containing satellite data with 'satellite_name', 'launch_year', and 'launch_month_year' columns.
        png_path (str, optional): The file path to save the plot as a PNG image. If None, the plot is not saved as a PNG.
        html_path (str, optional): The file path to save the plot as an HTML file. If None, the plot is not saved as an HTML file.

    Returns:
        None: The function displays the plot and optionally saves it as a PNG and/or HTML file.
    """
    display_line_plot(display_data=get_starlink_vs_other_launches(df), x_col='launch_month_year', y_col='launches', labels={
        'launch_month_year': 'Year',
        'launches': 'Number of Launches'
    }, title='Number of Starlink vs All Other Satellite Launches', color_sequence=['#2c57c9', '#c95574'], color_col='type', png_path=png_path, html_path=html_path)
