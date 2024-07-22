from joblib import load
import streamlit as st
from local import ARTIFACTS_PATH
from sat_growth_over_time import get_sat_growth_over_time_plot, get_starlink_vs_all_other_sats_plot
from annual_launches_by_country import get_annual_launches_by_org_plot
from annual_launches_by_sat_type import get_launch_count_by_sat_class_plot


@st.cache_data
def load_data(filepath):
    """
    Loads data from a specified file using Joblib.

    Parameters:
    filepath (str or Path): The path to the file containing the data to be loaded.

    Returns:
    object: The data loaded from the file, typically a Python object serialized with Joblib.

    The function opens the specified file in binary read mode, loads the data using Joblib, and returns the loaded data.
    """
    with open(filepath, 'rb') as f:
        return load(f)


# Dictionary to map filenames to functions
PLOTS = {
    "Satellite Growth Over Time": {
        "filename": "launch_decay_orbit_over_time",
        "function": get_sat_growth_over_time_plot
    },
    "Starlink vs All Other Satellites": {
        "filename": "starlink_vs_other_launches",
        "function": get_starlink_vs_all_other_sats_plot
    },
    "Annual Number of Launches by Country": {
        "filename": "annual_launches_by_country",
        "function": get_annual_launches_by_org_plot
    },
    "Annual Number of Launches by Satellite Type": {
        "filename": "launch_count_by_sat_class",
        "function": get_launch_count_by_sat_class_plot
    }
}


def render_plot(choice, data):
    """
    Renders the selected plot in the Streamlit app.

    Parameters:
    choice (str): The title of the plot to render, corresponding to a key in the PLOTS dictionary.
    data (dict): A dictionary containing the loaded data files, where keys are filenames and values are the data.

    Returns:
    None: The function directly renders the plot using Streamlit.

    The function retrieves the appropriate plot function and data based on the user's choice,
    generates the plot, and then displays it in the Streamlit app.
    """
    plot_info = PLOTS[choice]
    fig = plot_info["function"](display_data=data[plot_info["filename"]])
    st.plotly_chart(fig)


if __name__ == "__main__":
    # Load all data files into a dictionary
    data = {name: load_data(
        ARTIFACTS_PATH / f"{info['filename']}.joblib") for name, info in PLOTS.items()}

    st.title("Visualizations Dashboard")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    options = ["Home"] + list(PLOTS.keys())
    choice = st.sidebar.selectbox("Select a page", options)

    if choice == "Home":
        st.write("Welcome to the Visualizations Dashboard!")
    if choice == "Home":
        st.write("Welcome to the Visualizations Dashboard!")
    else:
        st.header(choice)
        render_plot(choice, data)
