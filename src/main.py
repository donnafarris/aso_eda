# Create your own local.py file in the src dir
from local import ARTIFACTS_PATH
from joblib import load
from os import listdir
from artifact_setup import make_artifacts
from sat_growth_over_time import display_sat_growth_over_time_plot, display_starlink_vs_all_other_sats_plot
from annual_launches_by_country import display_annual_launches_by_org_plot
from annual_launches_by_sat_type import display_launch_count_by_sat_class_plot
filenames = ['annual_launches_by_country',
             'launch_count_by_sat_class',
             'launch_decay_orbit_over_time',
             'starlink_vs_other_launches']
if any(element+'.joblib' not in listdir(ARTIFACTS_PATH) for element in filenames):
    make_artifacts()


def load_data(filepath):
    with open(filepath, 'rb') as f:
        return load(f)


data = {}
for filename in filenames:
    data[filename] = load_data(ARTIFACTS_PATH+filename+'.joblib')

display_sat_growth_over_time_plot(
    display_data=data['launch_decay_orbit_over_time'],
    png_path='../img/sat_growth.png',
    html_path='../img/sat_growth.html')
display_starlink_vs_all_other_sats_plot(
    display_data=data['starlink_vs_other_launches'],
    png_path='../img/starlink_vs_all_others.png',
    html_path='../img/starlink_vs_all_others.html')
display_annual_launches_by_org_plot(
    display_data=data['annual_launches_by_country'],
    png_path='../img/launches_by_country.png',
    html_path='../img/launches_by_country.html')
display_launch_count_by_sat_class_plot(
    display_data=data['launch_count_by_sat_class'],
    png_path='../img/launches_by_sat_type.png',
    html_path='../img/launches_by_sat_type.html')
