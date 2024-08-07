# app.py
from joblib import load
import streamlit as st
import os
import add_path
import requests
from src.annual_launches_by_sat_type import get_launch_count_by_sat_class_plot
from src.annual_launches_by_country import get_annual_launches_by_org_plot
from src.sat_growth_over_time import get_sat_growth_over_time_plot, get_starlink_vs_all_other_sats_plot
from src.local import ARTIFACTS_PATH


@st.cache_data
def load_data(filepath):
    with open(filepath, 'rb') as f:
        return load(f)


filenames = {
    'launch_decay_orbit_over_time': 'Satellite Growth Over Time',
    'starlink_vs_other_launches': 'Starlink vs All Other Satellites',
    'annual_launches_by_country': 'Annual Number of Launches by Country',
    'launch_count_by_sat_class': 'Annual Number of Launches by Satellite Type'
}

data = {key: load_data(os.path.join(ARTIFACTS_PATH, f"{key}.joblib"))
        for key in filenames.keys()}

plot_functions = {
    "Satellite Growth Over Time": get_sat_growth_over_time_plot,
    "Starlink vs All Other Satellites": get_starlink_vs_all_other_sats_plot,
    "Annual Number of Launches by Country": get_annual_launches_by_org_plot,
    "Annual Number of Launches by Satellite Type": get_launch_count_by_sat_class_plot
}

# Function to call the prediction API


def get_prediction(payload):
    url = 'http://127.0.0.1:8000/predict'
    response = requests.post(url, json=payload)
    return response.json()


if __name__ == "__main__":
    st.title("Artificial Space Objects Dashboard")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    options = ["Home", "Prediction Form"] + list(plot_functions.keys())
    choice = st.sidebar.selectbox("Select a page", options)

    if choice == "Home":
        st.write("Welcome to the ASO Dashboard!")
    elif choice == "Prediction Form":
        st.header("Prediction Form")

        with st.form(key='predict_form'):
            total_mass = st.number_input("Total Mass", value=0.0)
            span = st.number_input("Span", value=0.0)
            period_mins = st.number_input("Period Minutes", value=0.0)
            perigee_km = st.number_input("Perigee KM", value=0.0)
            apogee_km = st.number_input("Apogee KM", value=0.0)
            inclination = st.number_input("Inclination", value=0.0)
            object_type = st.selectbox("Object Type", options=[
                                       "PAY", "DEB", "R/B", "Unknown"])

            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            payload = {
                "total_mass": total_mass,
                "span": span,
                "period_mins": period_mins,
                "perigee_km": perigee_km,
                "apogee_km": apogee_km,
                "inclination": inclination,
                "object_type": object_type
            }
            prediction = get_prediction(payload)
            st.write("Prediction:", prediction)

    else:
        plot_func = plot_functions[choice]
        filename = list(filenames.keys())[
            list(filenames.values()).index(choice)]
        st.header(choice, anchor=filename)
        fig = plot_func(display_data=data[filename])
        st.plotly_chart(fig)
