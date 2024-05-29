import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    flights = pd.read_csv("data/flights.csv")
    airports = pd.read_csv("data/airports.csv")
    return flights, airports

def app():
    st.title("Visualizations")

    flights, airports = load_data()

    # Map plot of airports
    st.subheader('Map of Airports')
    fig1 = px.scatter_mapbox(airports, lat='LATITUDE', lon='LONGITUDE', hover_name='AIRPORT', hover_data=['CITY', 'STATE', 'COUNTRY'], zoom=3, title='Map of Airports')
    fig1.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig1)

    st.write(flights.columns)

    # For some plots random sample was chosen, because the data is too big, and it fails to plot for all
    delayed_flights = flights[flights['ARRIVAL_DELAY'] > 0]
    random_sample = delayed_flights.sample(n=100, random_state=42)

    # Departure delay vs arrival delay
    st.subheader('Departure Delay vs. Arrival Delay')
    fig2 = px.scatter(random_sample, x='DEPARTURE_DELAY', y='ARRIVAL_DELAY', color='AIRLINE', hover_name='ORIGIN_AIRPORT', title='Departure Delay vs. Arrival Delay')
    st.plotly_chart(fig2)

    # Scatter plot with animation by year, color by airline, and size by distance
    st.subheader('Animated Scatter Plot')
    fig3 = px.scatter(data_frame=random_sample, x='DEPARTURE_DELAY', y='ARRIVAL_DELAY', animation_frame='YEAR',
                      range_x=[-20, 100], color='AIRLINE', size='DISTANCE',
                      title='Animated Scatter Plot')
    st.plotly_chart(fig3)

    st.subheader('General Histograms and Bar Plots')

    # Departure delays
    fig4 = px.histogram(flights, x='DEPARTURE_DELAY', title='Distribution of Departure Delays', range_x=(-30, 60))
    st.plotly_chart(fig4)

    # Arrival delays
    fig5 = px.histogram(flights, x='ARRIVAL_DELAY', title='Distribution of Arrival Delays', range_x=(-70, 100), range_y=(0, 180000))
    st.plotly_chart(fig5)

    # The number of delayed flights per airline
    delayed_flight_count_by_airline = delayed_flights['AIRLINE'].value_counts().reset_index()
    delayed_flight_count_by_airline.columns = ['AIRLINE', 'COUNT']
    fig6 = px.bar(delayed_flight_count_by_airline, x='AIRLINE', y='COUNT', title='Number of Delayed Flights per Airline')
    st.plotly_chart(fig6)

    # The number of flight cancellations by reason
    reason_mapping = {'A': 'Airline/Carrier', 'B': 'Weather', 'C': 'National Air System', 'D': 'Security'}

    cancellation_reason_count = flights['CANCELLATION_REASON'].value_counts().reset_index()
    cancellation_reason_count.columns = ['CANCELLATION_REASON', 'COUNT']
    cancellation_reason_count['CANCELLATION_REASON'] = cancellation_reason_count['CANCELLATION_REASON'].map(reason_mapping)
    fig7 = px.bar(cancellation_reason_count, x='CANCELLATION_REASON', y='COUNT',
                 title='Flight Cancellations by Reason',
                 labels={'CANCELLATION_REASON': 'Cancellation Reason', 'COUNT': 'Count'})
    st.plotly_chart(fig7)
