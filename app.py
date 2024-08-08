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

st.set_page_config(page_title="Artificial Space Objects Dashboard")


@st.cache_data
def load_data(filepath):
    """Load data from a joblib file."""
    with open(filepath, 'rb') as f:
        return load(f)


# Dictionary to store filenames and their corresponding human-readable names
filenames = {
    'launch_decay_orbit_over_time': 'Satellite Growth Over Time',
    'starlink_vs_other_launches': 'Starlink vs All Other Satellites',
    'annual_launches_by_country': 'Annual Number of Launches by Country',
    'launch_count_by_sat_class': 'Annual Number of Launches by Satellite Type'
}

# Load data for each visualization
data = {key: load_data(os.path.join(ARTIFACTS_PATH, f"{key}.joblib"))
        for key in filenames.keys()}

# Dictionary to map visualization names to their corresponding functions
plot_functions = {
    "Satellite Growth Over Time": get_sat_growth_over_time_plot,
    "Starlink vs All Other Satellites": get_starlink_vs_all_other_sats_plot,
    "Annual Number of Launches by Country": get_annual_launches_by_org_plot,
    "Annual Number of Launches by Satellite Type": get_launch_count_by_sat_class_plot
}

# Define the mapping of prediction values to string values
status_mapping = {
    'O': 'In orbit',
    'D': 'Deorbited',
    'DK': 'Docked',
    'E': 'Exploded',
    'ERR': 'No tracking data',
    'L': 'Landed',
    'N': 'Renamed',
    'R': 'Reentered'
}


def get_prediction(payload):
    """
    Call the prediction API with the given payload.

    Args:
        payload (dict): Dictionary containing the input features.

    Returns:
        dict: API response containing the prediction.
    """
    url = 'https://aso-status-prediction-api.onrender.com/predict'
    response = requests.post(url, json=payload)
    return response.json()


def render_home():
    """Render the home page with an introduction and overview."""
    st.title("Artificial Space Objects Dashboard")
    st.markdown("""
    ## Welcome!
    Welcome to the **Artificial Space Objects (ASO) Dashboard**! This platform provides an in-depth look at the trends and patterns in the launch and distribution of artificial space objects over time.

    ### Overview
    This project involves:
    - **Exploratory Data Analysis (EDA):** Uncovering patterns, trends, and insights from tracked artificial space objects (ASOs).
    - **Predictive Modeling:** Training a machine learning model to predict the status of satellites based on their characteristics.

    ### Key Features
    - **Analyze:** Distribution of ASOs by country and organization.
    - **Identify:** Temporal trends in ASO launches.
    - **Predict:** Satellite status using machine learning techniques.

    ### Data Sources
    Our primary data sources are:
    - **[Celestrak](https://www.celestrak.com/)** for raw SATCAT data.
    - **[GCAT by Jonathan McDowell](https://www.planet4589.org/space/gcat/)** for a comprehensive catalog of artificial space objects.

    ### Visualizations
    Explore various visualizations to gain insights into:
    - Temporal trends in ASO launches.
    - Annual number of ASO launches by country.
    - Starlink satellites vs. all other satellites.
    - Satellite types launched over time.
                
    ### Prediction Model
    Our model, a Random Forest classifier, is trained to predict the status of satellites using features such as total mass, span, orbital parameters, and object type. The model is able to predict satellite status with a 92.4 percent accuracy.

    ### How to Use the App
    - **Home:** This page provides an overview of the ASO Dashboard.
    - **Prediction Form:** Use this form to input satellite characteristics and predict their status.
    - **Visualizations:** Explore various visualizations to understand trends and patterns in ASO data.

    ### Access the App
    Navigate through the app using the sidebar to explore data visualizations or use the prediction form to get satellite status predictions. Enjoy your exploration!
    """)


# st.image("https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2000/10/orbital_test_satellite_ots_-_artist_s_impression/9227956-5-eng-GB/Orbital_Test_Satellite_OTS_-_artist_s_impression.jpg",
#          caption="Orbital Test Satellite - artist's impression (2002)")


def render_prediction_form():
    """Render the prediction form for user input and display the prediction result."""
    st.header("Prediction Form")
    with st.form(key='predict_form'):
        col1, col2 = st.columns(2)
        with col1:
            object_type = st.selectbox("Object Type", options=[
                                       "PAY", "DEB", "R/B", "Unknown"])
            total_mass = st.number_input(
                "Total Mass (kg)", value=0.0, help="Enter the total mass of the object in kilograms.")
            span = st.number_input(
                "Span (m)", value=0.0, help="Enter the span of the object in meters.")
        with col2:
            period_mins = st.number_input(
                "Period (minutes)", value=0.0, help="Enter the orbital period in minutes.")
            perigee_km = st.number_input(
                "Perigee (km)", value=0.0, help="Enter the perigee distance in kilometers.")
            apogee_km = st.number_input(
                "Apogee (km)", value=0.0, help="Enter the apogee distance in kilometers.")
            inclination = st.number_input(
                "Inclination (degrees)", value=0.0, help="Enter the orbital inclination in degrees.")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        with st.spinner('Calculating...'):
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
            prediction_str = status_mapping.get(
                prediction.get('prediction'), 'Unknown')
            st.success(f"Prediction: {prediction_str}")


def render_visualizations():
    """Render the visualizations page for user to select and display different visualizations."""
    st.header("Visualizations")
    viz_choice = st.selectbox("Select a visualization",
                              list(plot_functions.keys()))
    if viz_choice:
        plot_func = plot_functions[viz_choice]
        filename = list(filenames.keys())[
            list(filenames.values()).index(viz_choice)]
        fig = plot_func(display_data=data[filename])
        st.plotly_chart(fig)


if __name__ == "__main__":
    # Sidebar navigation
    page = st.sidebar.radio(
        "Go to", ["Home", "Prediction Form", "Visualizations"])

    if page == "Home":
        render_home()
    elif page == "Prediction Form":
        render_prediction_form()
    elif page == "Visualizations":
        render_visualizations()
