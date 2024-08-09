# artifact_setup.py
from src.data_cleaning import generate_data_artifacts, df_dict_formatter
from src.data_ingestion import tsv_to_csv, csv_to_df_dict
from src.sat_growth_over_time import get_launch_decay_orbit_over_time, get_starlink_vs_other_launches
from src.annual_launches_by_country import get_annual_launches_by_country
from src.annual_launches_by_sat_type import get_launch_count_by_sat_class
from src.local import ARTIFACTS_PATH, DATA_PATH
from src.constants import ALL_COL_RENAME_DICTS


def get_data():
    """
    Process and return a dictionary of data artifacts from various sources.

    Returns:
        dict: A dictionary containing various data artifacts.
    """
    tsv_to_csv(DATA_PATH)
    df_dict = csv_to_df_dict(DATA_PATH)
    df_dict = df_dict_formatter(df_dict, ALL_COL_RENAME_DICTS)

    satcat_df = df_dict['celestrak_satcat_df']
    launch_df = df_dict['launch_df']
    orgs_df = df_dict['orgs_df']
    psatcat_df = df_dict['psatcat_df']

    launch_decay_orbit_over_time = get_launch_decay_orbit_over_time(satcat_df)
    starlink_vs_other_launches = get_starlink_vs_other_launches(satcat_df)
    annual_launches_by_country = get_annual_launches_by_country(
        launch_df, orgs_df)
    launch_count_by_sat_class = get_launch_count_by_sat_class(psatcat_df)

    data = {
        'launch_decay_orbit_over_time': launch_decay_orbit_over_time,
        'starlink_vs_other_launches': starlink_vs_other_launches,
        'annual_launches_by_country': annual_launches_by_country,
        'launch_count_by_sat_class': launch_count_by_sat_class
    }
    return data


def make_artifacts():
    """
    Generate and save data artifacts using joblib.

    Returns:
        None
    """
    data = get_data()
    for key, value in data.items():
        generate_data_artifacts(f"{ARTIFACTS_PATH}{key}.joblib", value)
