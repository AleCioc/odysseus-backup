
# from odysseus.dashboards.load_data import *
import streamlit as st
from datetime import date
from odysseus.city_data_manager.config.config import cities # get all possible city names from config files


def load_sidebar():
    
    city_name = st.sidebar.selectbox(
        'City:',
        cities
    )

    # st.sidebar.write(
    #     """ 
    #     # Hai scritto: {} """.format(city_name)
    # )

    
    # TODO need to change the list which is showed based on the city chosen 
    selected_month = st.sidebar.selectbox('Month', [10]) 
    # TODO need to change the list of years possible based on the available files
    selected_year = st.sidebar.selectbox('Year', [2017])

    selected_source = st.sidebar.selectbox('Source', ["big_data_db"])

    return city_name, selected_year, selected_month, selected_source
