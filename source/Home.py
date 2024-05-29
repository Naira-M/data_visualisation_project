import streamlit as st

st.title("Airline Data Dashboard")

PAGES = {
    "Data Exploration": "page1",
    "Flight Delays": "page2",
    "Flight Cancellations": "page3"
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
module = __import__(page)
module.app()
