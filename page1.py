import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

@st.cache_data
def load_data():
    airlines = pd.read_csv("data/airlines.csv")
    airports = pd.read_csv("data/airports.csv")
    flights = pd.read_csv("data/flights.csv")
    return airlines, airports, flights

def app():
    st.title("Data Exploration")

    airlines, airports, flights = load_data()

    # Explore airlines table
    st.header("Airlines Table")
    st.write("The number of airlines is", airlines.shape[0])
    st.write("Columns of the 'airlines' table: ", ', '.join(airlines.columns))
    st.write(airlines.head(2))
    st.write("The number of duplicated rows in 'airlines' table is", sum(airlines.duplicated()))
    st.write("Missing values in airlines table:")
    st.write(airlines.isnull().sum())

    # Explore airports table
    st.header("Airports Table")
    st.write("The number of airports is", airports.shape[0])
    st.write(airports.head(2))
    st.write("Missing values in airports table:")
    st.write(airports.isnull().sum())
    st.write("There are", airports["AIRPORT"].duplicated().sum(), "airports with the same name.")

    # Explore flights table
    st.header("Flights Table")
    st.write(f"There are {flights.shape[0]} rows, and {flights.shape[1]} columns.")
    st.write(flights.head(2))
    st.write("Missing values in flights table:")
    st.write(flights.isnull().sum())

    # Visualizations
    st.header("Visualizations")

    # Missing values bar plot
    st.subheader("Missing Values in Flights Table")
    fig1 = msno.bar(flights)
    st.pyplot(fig1.get_figure())

    st.write("Number of duplicate rows:", flights.duplicated().sum())

    # Number of cancelled flights
    n_cancelled = (flights["CANCELLED"] == 1).sum()
    st.write("The number of cancelled flights is", n_cancelled)

    # Distribution of departure delays
    st.subheader('Distribution of Departure Delays')
    fig2, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(flights['DEPARTURE_DELAY'].dropna(), bins=50, kde=True, ax=ax)
    ax.set_title('Distribution of Departure Delays')
    ax.set_xlabel('Departure Delay (minutes)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig2)

    # Correlation matrix
    st.subheader('Correlation Matrix (Numerical Columns)')
    numerical_columns = flights.select_dtypes(include=['number'])
    correlation_matrix = numerical_columns.corr()
    fig3, ax = plt.subplots(figsize=(18, 12))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title('Correlation Matrix (Numerical Columns)')
    st.pyplot(fig3)

    # Count of flights by airlines
    st.subheader('Number of Flights by Airline')
    fig4, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(y='AIRLINE', data=flights, order=flights['AIRLINE'].value_counts().index, ax=ax)
    ax.set_title('Number of Flights by Airline')
    ax.set_xlabel('Number of Flights')
    ax.set_ylabel('Airline')
    st.pyplot(fig4)
