import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

@st.cache_data
def create_heatmap(data, x_field, y_field, x_filter, y_filter):
    if x_field == y_field:
        st.error("Please select different fields for the x-axis and y-axis.")
        return None
    filtered_data = data[data[x_field].isin(x_filter) & data[y_field].isin(y_filter)]
    if x_field == 'ResponseTimeMinutes':
        filtered_data[x_field] = pd.cut(filtered_data[x_field], bins=[0, 30, 60, 120, float('inf')], 
                                        labels=['0-30', '31-60', '61-120', '121+'], include_lowest=True)
    heatmap_data = filtered_data.groupby([x_field, y_field]).agg(
        csat_score=('CSATScore', 'mean'),
        ticket_volume=('CSATScore', 'count')
    ).reset_index()
    x_values = sorted(heatmap_data[x_field].unique())
    y_values = sorted(heatmap_data[y_field].unique(), reverse=True)
    heatmap_matrix = np.zeros((len(y_values), len(x_values)))
    ticket_volume_matrix = np.zeros((len(y_values), len(x_values)))
    for _, row in heatmap_data.iterrows():
        x_index = x_values.index(row[x_field])
        y_index = y_values.index(row[y_field])
        heatmap_matrix[y_index, x_index] = row['csat_score']
        ticket_volume_matrix[y_index, x_index] = row['ticket_volume']
    total_tickets = ticket_volume_matrix.sum()
    ticket_percentage_matrix = ticket_volume_matrix / total_tickets * 100
    hovertemplate = '<b>%{x}</b><br><b>%{y}</b><br>CSAT Score: %{z:.2f}<br>Ticket Volume: %{customdata[0]}<br>Percentage of Total Tickets: %{customdata[1]:.2f}%<extra></extra>'
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_matrix,
        x=x_values,
        y=y_values,
        customdata=np.dstack((ticket_volume_matrix, ticket_percentage_matrix)),
        colorscale='RdYlGn',
        hovertemplate=hovertemplate,
        colorbar=dict(title='CSAT Score')
    ))
    fig.update_layout(
        title=f'CSAT Score Heatmap: {x_field} vs {y_field}',
        xaxis_title=x_field,
        yaxis_title=y_field,
        width=800,
        height=800
    )
    return fig

def render_heatmap(data):
    st.title('CSAT Score Heatmap Comparison')

    col1, col2 = st.columns(2)

    if st.button('Reset Filters'):
        st.session_state.x_field = 'ProductCategory'
        st.session_state.y_field = 'AgentTenure'
        st.session_state.x_filter = list(data['ProductCategory'].unique())
        st.session_state.y_filter = list(data['AgentTenure'].unique())

    with col1:
        st.subheader('Side A (X-axis)')
        x_field = st.selectbox('Select Field', fields, key='x_field', index=fields.index('ProductCategory'))
        x_filter_options = data[x_field].unique()
        x_filter = st.multiselect(f'Filter {x_field}', x_filter_options, default=x_filter_options, key='x_filter')
        
        filtered_data_a = data[data[x_field].isin(x_filter)]
        total_tickets_a = len(filtered_data_a)
        avg_csat_score_a = filtered_data_a['CSATScore'].mean()
        
        st.metric(label="Total Tickets", value=total_tickets_a)
        st.metric(label="Average CSAT Score", value=f"{avg_csat_score_a:.2f}")

    with col2:
        st.subheader('Side B (Y-axis)')
        y_field = st.selectbox('Select Field', fields, key='y_field', index=fields.index('AgentTenure'))
        y_filter_options = data[y_field].unique()
        y_filter = st.multiselect(f'Filter {y_field}', y_filter_options, default=y_filter_options, key='y_filter')
        
        filtered_data_b = data[data[y_field].isin(y_filter)]
        total_tickets_b = len(filtered_data_b)
        avg_csat_score_b = filtered_data_b['CSATScore'].mean()
        
        st.metric(label="Total Tickets", value=total_tickets_b)
        st.metric(label="Average CSAT Score", value=f"{avg_csat_score_b:.2f}")
    
    filtered_data = data[data[x_field].isin(x_filter) & data[y_field].isin(y_filter)]
    heatmap_fig = create_heatmap(filtered_data, x_field, y_field, x_filter, y_filter)

    if heatmap_fig:
        st.plotly_chart(heatmap_fig, use_container_width=True)
            
        csv_data = filtered_data
        csv = csv_data.to_csv(index=False)
        st.download_button(
            label='Export Data',
            data=csv,
            file_name='heatmap_data.csv',
            mime='text/csv'
        )
    else:
        st.warning('Please select valid fields and filters to generate the heatmap.')

fields = ['ChannelName', 'TicketCategory', 'TicketSubCategory', 'ResponseTimeMinutes', 'ProductCategory',
          'SupervisorName', 'ManagerName', 'AgentTenure', 'AgentShift']
