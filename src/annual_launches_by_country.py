from data_cleaning import col_val_mapper
from helpers import display_bar_plot
from constants import ALL_VAL_RENAME_DICTS


def add_launch_country_col(launch_df, orgs_df):
    """
    Adds a 'launch_country' column to the launch DataFrame based on the organization codes.

    This function maps organization codes in the `launch_df` DataFrame to country names by using the 
    `state_code` and `state_name` in the `orgs_df` DataFrame. It utilizes the `col_val_mapper` function 
    to rename state codes to state names and then creates a mapping from organization codes to country names.

    Args:
        launch_df (pd.DataFrame): The DataFrame containing launch data with 'launch_agency' column.
        orgs_df (pd.DataFrame): The DataFrame containing organization data with 'org_code' and 'state_code' columns.

    Returns:
        pd.DataFrame: The launch DataFrame with an added 'launch_country' column containing country names.
    """
    orgs_df = col_val_mapper(orgs_df, 'state_code',
                             'state_name', ALL_VAL_RENAME_DICTS)
    # Create dict to map on
    orgs_df[['org_code', 'state_name']].to_dict(
        orient='split', index=False, into=dict)
    source_mapping = orgs_df.set_index('org_code')['state_name'].to_dict()
    # Map the dict onto launch_agency to create the values for launch_country
    launch_df.loc[:, 'launch_country'] = launch_df['launch_agency'].map(
        source_mapping)
    return launch_df


def get_annual_launches_by_country(launch_df, orgs_df):
    """
    Calculates the annual number of satellite launches by country.

    This function filters the launch DataFrame to include only operational satellites, adds a column for the launch country,
    and groups the data by launch year and country to count the number of launches each year. It uses the organization DataFrame
    to map organization codes to country names.

    Args:
        launch_df (pd.DataFrame): The DataFrame containing launch data with 'launch_code' and 'Julian_Date' columns.
        orgs_df (pd.DataFrame): The DataFrame containing organization data with 'org_code' and 'state_code' columns.

    Returns:
        pd.DataFrame: A DataFrame with the annual count of satellite launches by country.
    """
    # Ensure no missing values in essential columns
    launch_df = launch_df.dropna(subset=['launch_code', 'Julian_Date'])
    orgs_df = orgs_df.dropna(subset=['org_code', 'state_code'])
    # 'O' in launch_code means the mission was orbital
    # 'S' after 'O' indicates mission success
    launch_df = launch_df[launch_df['launch_code'].str.startswith('OS')].copy()
    # Add country and launch_year columns to filter on
    launch_df = add_launch_country_col(launch_df, orgs_df)
    launch_df['launch_year'] = launch_df['Julian_Date'].dt.year
    # Add launch_entity column to group some countries by NATO affiliation
    launch_df = col_val_mapper(
        launch_df, 'launch_country', 'launch_entity', ALL_VAL_RENAME_DICTS)
    annual_launches = launch_df.groupby(
        ['launch_year', 'launch_entity']).size().reset_index(name='launch_count')
    # Only show entities with 1 or more launches
    annual_launches = annual_launches[(annual_launches['launch_count'] > 0)]
    return annual_launches


def display_annual_launches_by_org_plot(launch_df, orgs_df, png_path=None, html_path=None):
    """
    Displays a bar plot of the annual number of satellite launches by country and optionally saves the plot as a PNG and HTML file.

    This function generates and displays a bar plot using Plotly Express, showing the annual number of satellite launches
    for each country. It utilizes the `get_annual_launches_by_country` function to obtain the data, grouping by launch year 
    and country. Optionally, it saves the plot as a PNG and/or HTML file if paths are provided.

    Args:
        launch_df (pd.DataFrame): The DataFrame containing launch data with 'launch_code' and 'Julian_Date' columns.
        orgs_df (pd.DataFrame): The DataFrame containing organization data with 'org_code' and 'state_code' columns.
        png_path (str, optional): The file path to save the plot as a PNG image. If None, the plot is not saved as a PNG.
        html_path (str, optional): The file path to save the plot as an HTML file. If None, the plot is not saved as an HTML file.

    Returns:
        None: The function displays the plot and optionally saves it as a PNG and/or HTML file.
    """
    display_bar_plot(display_data=get_annual_launches_by_country(launch_df, orgs_df),
                     color_col_name='launch_entity', title='Annual Number of Launches by Country', png_path=png_path, html_path=html_path)
