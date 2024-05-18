import streamlit as st
import plotly.graph_objects as go

def create_mirrored_bar_chart(data, num_agents, weight_by_volume):
    # Data Preparation
    agent_data = data.groupby('AgentName').agg({'CSATScore': ['mean', 'count']}).reset_index()
    agent_data.columns = ['AgentName', 'AvgCSATScore', 'InteractionVolume']
    agent_data = agent_data.sort_values('AvgCSATScore', ascending=False)

    # Data Filtering
    top_agents = agent_data.head(num_agents)
    bottom_agents = agent_data.tail(num_agents)
    if weight_by_volume:
        top_agents['AvgCSATScore'] *= top_agents['InteractionVolume']
        bottom_agents['AvgCSATScore'] *= bottom_agents['InteractionVolume']

    # Chart Creation
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_agents['AgentName'],
        x=top_agents['AvgCSATScore'],
        orientation='h',
        marker_color='green',
        name='Top Agents'
    ))
    fig.add_trace(go.Bar(
        y=bottom_agents['AgentName'],
        x=bottom_agents['AvgCSATScore'],
        orientation='h',
        marker_color='red',
        name='Bottom Agents'
    ))
    fig.update_layout(
        title='Top and Bottom Agents by CSAT Score',
        xaxis_title='CSAT Score',
        yaxis_title='Agent Name',
        yaxis=dict(autorange='reversed'),
        height=max(500, num_agents * 50),
        barmode='group',
        bargap=0.1
    )
    return fig

def mirrored_bar_chart(data):
    num_agents = st.selectbox('Number of Agents', [5, 10, 20, 50, 'All'])
    if num_agents == 'All':
        num_agents = len(data['AgentName'].unique())
    else:
        num_agents = int(num_agents)

    weight_by_volume = st.checkbox('Weight by Interaction Volume')

    fig = create_mirrored_bar_chart(data, num_agents, weight_by_volume)
    st.plotly_chart(fig, use_container_width=True)

def render_mirrored_bar_chart(data):
    st.title('Mirrored Bar Chart: Top and Bottom Agents')
    st.write('This chart displays the top and bottom agents based on their average CSAT scores.')
    st.write('The dropdown menu allows you to select the number of agents to display for each category.')
    st.write('The weighting toggle adjusts the CSAT scores based on the interaction volume of each agent.')
    mirrored_bar_chart(data)