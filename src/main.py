# main.py
from joblib import load
from os import listdir
from src.artifact_setup import make_artifacts
from src.sat_growth_over_time import display_sat_growth_over_time_plot, display_starlink_vs_all_other_sats_plot
from src.annual_launches_by_country import display_annual_launches_by_org_plot
from src.annual_launches_by_sat_type import display_launch_count_by_sat_class_plot
from src.local import ARTIFACTS_PATH


def check_and_create_artifacts(filenames):
    """
    Check if artifact files exist and create them if they do not.

    Args:
        filenames (list): List of artifact filenames to check.
    """
    if any(f'{filename}.joblib' not in listdir(ARTIFACTS_PATH) for filename in filenames):
        make_artifacts()


def load_data(filepath):
    """
    Load data from a joblib file.

    Args:
        filepath (str): The path to the joblib file.

    Returns:
        Any: The data loaded from the joblib file.
    """
    with open(filepath, 'rb') as f:
        return load(f)


def main():
    filenames = [
        'annual_launches_by_country',
        'launch_count_by_sat_class',
        'launch_decay_orbit_over_time',
        'starlink_vs_other_launches'
    ]

    check_and_create_artifacts(filenames)

    data = {filename: load_data(f'{ARTIFACTS_PATH}{filename}.joblib')
            for filename in filenames}

    display_sat_growth_over_time_plot(
        display_data=data['launch_decay_orbit_over_time'],
        png_path='../img/sat_growth.png',
        html_path='../img/sat_growth.html'
    )

    display_starlink_vs_all_other_sats_plot(
        display_data=data['starlink_vs_other_launches'],
        png_path='../img/starlink_vs_all_others.png',
        html_path='../img/starlink_vs_all_others.html'
    )

    display_annual_launches_by_org_plot(
        display_data=data['annual_launches_by_country'],
        png_path='../img/launches_by_country.png',
        html_path='../img/launches_by_country.html'
    )

    display_launch_count_by_sat_class_plot(
        display_data=data['launch_count_by_sat_class'],
        png_path='../img/launches_by_sat_type.png',
        html_path='../img/launches_by_sat_type.html'
    )


if __name__ == '__main__':
    main()
