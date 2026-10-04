import pandas as pd
import streamlit as st


@st.cache_data
def load_temperature():
    return pd.read_csv("datasets/GlobalLandTemperaturesByCountry.csv")


@st.cache_data
def load_air_quality():

    air = pd.read_csv("datasets/city_day.csv")

    air = air.sort_values("Date")

    return air


@st.cache_data
def load_co2():
    return pd.read_csv("datasets/owid-co2-data.csv")