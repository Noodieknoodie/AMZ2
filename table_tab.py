import streamlit as st
import pandas as pd

def display_data_table(data):
    st.title("Data Table View")
    sort_option = st.selectbox('Sort by:', [''] + list(data.columns))
    if sort_option:
        data = data.sort_values(by=sort_option)
    st.dataframe(data, height=600)  # Adjust height as needed