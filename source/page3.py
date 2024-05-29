import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    flights = pd.read_csv("data/flights.csv")
    return flights


def app():
    flights = load_data()
    st.subheader('Flight Cancellations')

    # Convert YEAR, MONTH to a datetime column for easier plotting over time
    flights['DATE'] = pd.to_datetime(flights[['YEAR', 'MONTH']].assign(DAY=1))

    # Filter out only cancelled flights
    cancelled_flights = flights[flights['CANCELLED'] == 1]

    # The number of flight cancellations by reason
    reason_mapping = {'A': 'Airline/Carrier', 'B': 'Weather', 'C': 'National Air System', 'D': 'Security'}

    cancellation_reason_count = flights['CANCELLATION_REASON'].value_counts().reset_index()
    cancellation_reason_count.columns = ['CANCELLATION_REASON', 'COUNT']
    cancellation_reason_count['CANCELLATION_REASON'] = cancellation_reason_count['CANCELLATION_REASON'].map(
        reason_mapping)
    fig1 = px.bar(cancellation_reason_count, x='CANCELLATION_REASON', y='COUNT',
                  title='Flight Cancellations by Reason',
                  labels={'CANCELLATION_REASON': 'Cancellation Reason', 'COUNT': 'Count'})
    st.plotly_chart(fig1)

    # Cancellations Over Time
    cancellations_over_time = cancelled_flights.groupby('DATE').size().reset_index(name='Cancellations')
    fig2 = px.line(cancellations_over_time, x='DATE', y='Cancellations', title='Number of Cancellations Over Time')
    st.plotly_chart(fig2)

    # The number of flight cancellations by airlines
    cancellation_by_airlines_count = flights['AIRLINE'].value_counts().reset_index()

    cancellation_by_airlines_count.columns = ['AIRLINE', 'COUNT']
    fig1 = px.bar(cancellation_by_airlines_count, x='AIRLINE', y='COUNT',
                  title='Flight Cancellations per Airline',
                  labels={'AIRLINE': 'Airline', 'COUNT': 'Count'})
    st.plotly_chart(fig1)
