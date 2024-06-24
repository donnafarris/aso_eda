# Create your own local.py file in the src dir
from local import DATA_PATH
from constants import ALL_COL_RENAME_DICTS
from data_cleaning import df_dict_formatter
from data_ingestion import tsv_to_csv, csv_to_df_dict
from sat_growth_over_time import display_sat_growth_over_time_plot, display_starlink_vs_all_other_sats_plot
from annual_launches_by_country import display_annual_launches_by_org_plot
from annual_launches_by_sat_type import display_launch_count_by_sat_class_plot
tsv_to_csv(DATA_PATH)
df_dict = csv_to_df_dict(DATA_PATH)
df_dict = df_dict_formatter(df_dict, ALL_COL_RENAME_DICTS)
satcat_df = df_dict['celestrak_satcat_df']
display_sat_growth_over_time_plot(satcat_df)
display_starlink_vs_all_other_sats_plot(satcat_df)
launch_df, orgs_df = df_dict['launch_df'], df_dict['orgs_df']
display_annual_launches_by_org_plot(launch_df, orgs_df)
psatcat_df = df_dict['psatcat_df']
display_launch_count_by_sat_class_plot(psatcat_df)
