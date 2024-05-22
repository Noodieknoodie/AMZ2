import streamlit as st
import pandas as pd
from table_tab import display_data_table
from mirrored_bar_chart import render_mirrored_bar_chart
from exploratory_data_analysis_2 import (
    plot_csat_score_distribution,
    plot_agent_tenure_vs_csat_score,
    plot_product_category_vs_csat_score,
    plot_response_time_vs_csat_score,
    generate_customer_remarks_wordcloud,
    plot_missing_data_impact
)
from heatmap import render_heatmap

st.set_page_config(layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("style.css")

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/RawAmazonData.csv')
        data.loc[data['ProductCategory'].isna(), 'ProductCategory'] = 'No Product Category'
        data.loc[data['AgentShift'].isna(), 'AgentShift'] = 'No Agent Shift'
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

data = load_data()

filters = {
    'selected_channels': [],
    'selected_products': [],
    'selected_shifts': []
}

def initialize_state():
    if 'init' not in st.session_state:
        channel_list = data['ChannelName'].unique().tolist()
        product_list = data['ProductCategory'].unique().tolist()
        shift_list = data['AgentShift'].unique().tolist()
        st.session_state.update({
            'selected_channels': channel_list,
            'selected_products': product_list,
            'selected_shifts': shift_list,
            'select_all_channels': True,
            'select_all_products': True,
            'select_all_shifts': True,
            'init': True,
            'previous_filters': None
        })

initialize_state()

tab_home, tab_data_table, tab_eda, tab_mirrored_chart, tab_heatmap = st.tabs(['Home', 'Data Table', 'Exploratory Data Analysis', 'Mirrored Bar Chart', 'Heatmap'])

def filter_section(key, options, title):
    with st.sidebar.expander(title):
        select_all_key = f'select_all_{key}'
        selected_items_key = f'selected_{key}'

        if selected_items_key not in st.session_state:
            st.session_state[selected_items_key] = options.tolist()

        def update_selected_items():
            if st.session_state[select_all_key]:
                st.session_state[selected_items_key] = options.tolist()
            else:
                st.session_state[selected_items_key] = []

        st.checkbox('Select All', value=st.session_state.get(select_all_key, True), key=select_all_key, on_change=update_selected_items)

        def update_select_all():
            all_selected = set(st.session_state[selected_items_key]) == set(options)
            st.session_state[select_all_key] = all_selected

        selected_items = st.multiselect(f'Select {title}:', options=options, default=st.session_state[selected_items_key], key=selected_items_key, on_change=update_select_all)
        return selected_items

if st.session_state.get('active_tab') != 'Heatmap':
    selected_channels = filter_section('channels', data['ChannelName'].unique(), 'Channels')
    selected_products = filter_section('products', data['ProductCategory'].unique(), 'Product Categories')
    selected_shifts = filter_section('shifts', data['AgentShift'].unique(), 'Agent Shifts')

    st.session_state['previous_filters'] = {
        'selected_channels': selected_channels,
        'selected_products': selected_products,
        'selected_shifts': selected_shifts,
    }
else:
    st.sidebar.write("Use the filters on the Heatmap dashboard.")

with tab_home:
    st.title('Team Amazon Dashboard for B BUS 441 A')
    st.subheader('University of Washington')
    st.write('Professor: Nick Cuhaciyan, Professor at University of Washington')
    st.write('Team Members: Ahmed Mohamad, Cyrus Cheng, Daniel Kulik, Erik Lars Knudsen, Gavin Fisher Detert, Osvaldo Flores, Teyonna Fegler, Trevon Sorlin Gagnon')

with tab_data_table:
    if st.session_state.get('active_tab') != 'Heatmap':
        filters = st.session_state['previous_filters']
        if len(filters['selected_channels']) == 0 or len(filters['selected_products']) == 0 or len(filters['selected_shifts']) == 0:
            st.warning("Please select at least one option in each category.")
        else:
            filtered_data = data[
                (data['ChannelName'].isin(filters['selected_channels'])) &
                (data['ProductCategory'].isin(filters['selected_products'])) &
                (data['AgentShift'].isin(filters['selected_shifts']))
            ]
            display_data_table(filtered_data)

with tab_eda:
    if st.session_state.get('active_tab') != 'Heatmap':
        filters = st.session_state['previous_filters']
        if len(filters['selected_channels']) == 0 or len(filters['selected_products']) == 0 or len(filters['selected_shifts']) == 0:
            st.warning("Please select at least one option in each category.")
        else:
            filtered_data = data[
                (data['ChannelName'].isin(filters['selected_channels'])) &
                (data['ProductCategory'].isin(filters['selected_products'])) &
                (data['AgentShift'].isin(filters['selected_shifts']))
            ]
            st.plotly_chart(plot_csat_score_distribution(filtered_data), use_container_width=True)
            st.plotly_chart(plot_agent_tenure_vs_csat_score(filtered_data), use_container_width=True)
            st.plotly_chart(plot_product_category_vs_csat_score(filtered_data), use_container_width=True)
            st.plotly_chart(plot_response_time_vs_csat_score(filtered_data), use_container_width=True)
            st.image(generate_customer_remarks_wordcloud(filtered_data).to_array(), use_column_width=True)
            st.plotly_chart(plot_missing_data_impact(filtered_data), use_container_width=True)

with tab_mirrored_chart:
    if st.session_state.get('active_tab') != 'Heatmap':
        filters = st.session_state['previous_filters']
        if len(filters['selected_channels']) == 0 or len(filters['selected_products']) == 0 or len(filters['selected_shifts']) == 0:
            st.warning("Please select at least one option in each category.")
        else:
            filtered_data = data[
                (data['ChannelName'].isin(filters['selected_channels'])) &
                (data['ProductCategory'].isin(filters['selected_products'])) &
                (data['AgentShift'].isin(filters['selected_shifts']))
            ]
            render_mirrored_bar_chart(filtered_data)

with tab_heatmap:
    st.session_state['active_tab'] = 'Heatmap'
    st.session_state.pop('previous_filters', None)
    render_heatmap(data)

st.session_state['active_tab'] = None