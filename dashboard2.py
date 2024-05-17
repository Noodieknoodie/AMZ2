import streamlit as st
import pandas as pd
from table_tab import display_data_table

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/RawAmazonData.csv')
        data['ProductCategory'].fillna('No Product Category', inplace=True)
        data['AgentShift'].fillna('No Agent Shift', inplace=True)
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure

data = load_data()

def initialize_state():
    if 'init' not in st.session_state:
        st.session_state.update({
            'selected_channels': data['ChannelName'].unique().tolist(),
            'selected_products': data['ProductCategory'].unique().tolist(),
            'selected_shifts': data['AgentShift'].unique().tolist(),
            'init': True,
        })

initialize_state()

tab_home, tab_data_table = st.tabs(['Home', 'Data Table'])

if st.session_state.get('show_filters', True):
    st.sidebar.header('Filter Options')
    def filter_section(key, options, title):
        with st.sidebar.expander(title):
            select_all = st.checkbox('Select All', True, key=f'select_all_{key}')
            return st.multiselect(f'Select {title}:', options=options, 
                                  default=options if select_all else [], key=key)

    selected_channels = filter_section('channels', data['ChannelName'].unique(), 'Channels')
    selected_products = filter_section('products', data['ProductCategory'].unique(), 'Product Categories')
    selected_shifts = filter_section('shifts', data['AgentShift'].unique(), 'Agent Shifts')

with tab_home:
    st.title('Team Amazon Dashboard for B BUS 441 A')
    st.subheader('University of Washington')
    st.write('Professor: Nick Cuhaciyan, Professor at University of Washington')
    st.write('Team Members: Ahmed Mohamad, Cyrus Cheng, Daniel Kulik, Erik Lars Knudsen, Gavin Fisher Detert, Osvaldo Flores, Teyonna Fegler, Trevon Sorlin Gagnon')

with tab_data_table:
    if not selected_channels or not selected_products or not selected_shifts:
        st.warning("Please select at least one option in each category.")
    else:
        filtered_data = data[
            (data['ChannelName'].isin(selected_channels)) &
            (data['ProductCategory'].isin(selected_products)) &
            (data['AgentShift'].isin(selected_shifts))
        ]
        display_data_table(filtered_data)