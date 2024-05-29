import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px


@st.cache_data
def load_data():
    flights = pd.read_csv("data/flights.csv")
    airports = pd.read_csv("data/airports.csv")
    return flights, airports


def app():

    flights, airports = load_data()

    st.subheader('Flight Delays')
    # Departure delays
    fig, ax = plt.subplots()
    sns.kdeplot(flights['DEPARTURE_DELAY'], ax=ax, fill=True, color='blue')
    ax.set_xlim(-30, 60)
    ax.set_title('Distribution of Departure Delays')
    ax.set_xlabel('Departure Delay (minutes)')
    ax.set_ylabel('Density')
    st.pyplot(fig)

    # Arrival delays
    fig, ax = plt.subplots()
    sns.kdeplot(flights['ARRIVAL_DELAY'], ax=ax, fill=True, color='green')
    ax.set_xlim(-70, 100)
    ax.set_title('Distribution of Arrival Delays')
    ax.set_xlabel('Arrival Delay (minutes)')
    ax.set_ylabel('Density')
    st.pyplot(fig)

    # For some plots random sample was chosen, because the data is too big, and it fails to plot for all
    delayed_flights = flights[flights['ARRIVAL_DELAY'] > 0]
    random_sample = delayed_flights.sample(n=100, random_state=42)
    random_sample_sorted = random_sample.sort_values(by=['MONTH'])
    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    random_sample_sorted['MONTH'] = random_sample_sorted['MONTH'].apply(lambda x: month_order[x - 1])
    random_sample_sorted['MONTH'] = pd.Categorical(random_sample_sorted['MONTH'], categories=month_order, ordered=True)

    # Scatter plot with animation by year, color by airline, and size by distance
    fig2 = px.scatter(data_frame=random_sample_sorted, x='DEPARTURE_DELAY', y='ARRIVAL_DELAY',
                      animation_frame='MONTH', title='Departure Delay vs. Arrival Delay',
                      range_x=[-20, 100], color='AIRLINE', size='DISTANCE')
    st.plotly_chart(fig2)

    departure_delays_per_month = (
        random_sample_sorted
        .groupby(['MONTH', 'AIRLINE'])
        .size()
        .reset_index(name='NUM_DEPARTURE_DELAYS')
    )

    # Create the animated scatter plot
    fig3 = px.scatter(
        data_frame=departure_delays_per_month,
        x='AIRLINE',
        y='NUM_DEPARTURE_DELAYS',
        animation_frame='MONTH',
        size='NUM_DEPARTURE_DELAYS',
        color='AIRLINE',
        title='Number of Departure Delays per Month',
        labels={'NUM_DEPARTURE_DELAYS': 'Number of Departure Delays', 'MONTH': 'Month', 'AIRLINE': 'Airline'}
    )
    st.plotly_chart(fig3)

    # The number of delayed flights per airline
    delayed_flight_count_by_airline = delayed_flights['AIRLINE'].value_counts().reset_index()
    delayed_flight_count_by_airline.columns = ['AIRLINE', 'COUNT']
    fig6 = px.bar(delayed_flight_count_by_airline, x='AIRLINE', y='COUNT',
                  title='Number of Delayed Flights per Airline')
    st.plotly_chart(fig6)

