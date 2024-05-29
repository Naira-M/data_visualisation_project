import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import plotly.express as px


@st.cache_data
def load_data():
    airlines = pd.read_csv("data/airlines.csv")
    airports = pd.read_csv("data/airports.csv")
    flights = pd.read_csv("data/flights.csv")
    return airlines, airports, flights


def app():
    airlines, airports, flights = load_data()

    st.subheader("About Data")
    st.write(f"The number of airlines: {airlines.shape[0]}")
    st.write(f"The number of airports: {airports.shape[0]}")
    st.write(f"There are {flights.shape[0]} rows and {flights.shape[1]} columns.")
    st.write(f"The number of cancelled flights: {(flights['CANCELLED'] == 1).sum()}")

    # Missing values bar plot
    st.subheader("Missing Values in Flights Table")
    fig1 = msno.bar(flights)
    st.pyplot(fig1.get_figure())

    # Correlation matrix
    st.subheader("Correlation Matrix Of Numerical Columns")
    numerical_columns = flights.select_dtypes(include=['number'])
    correlation_matrix = numerical_columns.corr()
    fig3, ax = plt.subplots(figsize=(18, 12))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title("Correlation Matrix (Numerical Columns)")
    st.pyplot(fig3)

    # Count of flights by airlines
    st.subheader("Number of Flights by Airline")
    fig4, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(y='AIRLINE', data=flights, order=flights['AIRLINE'].value_counts().index, ax=ax)
    ax.set_title("Number of Flights by Airline")
    ax.set_xlabel("Number of Flights")
    ax.set_ylabel("Airline")
    st.pyplot(fig4)

    # Map plot of airports
    st.subheader('Map of Airports')
    fig1 = px.scatter_mapbox(airports, lat='LATITUDE', lon='LONGITUDE', hover_name='AIRPORT',
                             hover_data=['CITY', 'STATE', 'COUNTRY'], zoom=3)
    fig1.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig1)