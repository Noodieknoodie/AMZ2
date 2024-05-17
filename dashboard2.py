# dashboard2.py
import streamlit as st
import pandas as pd
from table_tab import display_data_table
from exploratory_data_analysis_2 import (
    plot_csat_score_distribution,
    plot_agent_tenure_vs_csat_score,
    plot_product_category_vs_csat_score,
    plot_response_time_vs_csat_score,
    generate_customer_remarks_wordcloud,
    plot_missing_data_impact
)

st.set_page_config(layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/RawAmazonData.csv')
        data = data.copy()
        data.loc[data['ProductCategory'].isna(), 'ProductCategory'] = 'No Product Category'
        data.loc[data['AgentShift'].isna(), 'AgentShift'] = 'No Agent Shift'
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

tab_home, tab_data_table, tab_eda = st.tabs(['Home', 'Data Table', 'Exploratory Data Analysis'])

if st.session_state.get('show_filters', True):
    st.sidebar.header('Filter Options')

def filter_section(key, options, title):
    with st.sidebar.expander(title):
        select_all = st.checkbox('Select All', True, key=f'select_all_{key}')
        return st.multiselect(f'Select {title}:', options=options, default=options if select_all else [], key=key)

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

with tab_eda:
    if not selected_channels or not selected_products or not selected_shifts:
        st.warning("Please select at least one option in each category.")
    else:
        filtered_data = data[
            (data['ChannelName'].isin(selected_channels)) &
            (data['ProductCategory'].isin(selected_products)) &
            (data['AgentShift'].isin(selected_shifts))
        ]
        st.plotly_chart(plot_csat_score_distribution(filtered_data), use_container_width=True)
        st.plotly_chart(plot_agent_tenure_vs_csat_score(filtered_data), use_container_width=True)
        st.plotly_chart(plot_product_category_vs_csat_score(filtered_data), use_container_width=True)
        st.plotly_chart(plot_response_time_vs_csat_score(filtered_data), use_container_width=True)
        st.image(generate_customer_remarks_wordcloud(filtered_data).to_array(), use_column_width=True)
        st.plotly_chart(plot_missing_data_impact(filtered_data), use_container_width=True)
