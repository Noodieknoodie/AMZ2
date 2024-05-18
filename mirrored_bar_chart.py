import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def create_mirrored_bar_chart(data, employee_type, num_employees, weight_by_volume):
    employee_data = data.groupby(employee_type).agg({'CSATScore': ['mean', 'count']}).reset_index()
    employee_data.columns = [employee_type, 'AvgCSATScore', 'InteractionVolume']

    if weight_by_volume:
        # Calculate weighted average
        employee_data['WeightedAvgCSATScore'] = (employee_data['AvgCSATScore'] * employee_data['InteractionVolume']) / employee_data['InteractionVolume'].sum()
        
        # Normalize to the 1-5 scale
        max_score = employee_data['WeightedAvgCSATScore'].max()
        min_score = employee_data['WeightedAvgCSATScore'].min()
        employee_data['WeightedAvgCSATScore'] = 1 + 4 * (employee_data['WeightedAvgCSATScore'] - min_score) / (max_score - min_score) if max_score != min_score else 1

        employee_data = employee_data.sort_values('WeightedAvgCSATScore', ascending=False)
    else:
        employee_data = employee_data.sort_values('AvgCSATScore', ascending=False)

    if employee_type == 'ManagerName':
        top_employees = employee_data
        bottom_employees = None
    else:
        top_employees = employee_data.head(num_employees)
        bottom_employees = employee_data.tail(num_employees)

    colors = px.colors.sequential.Viridis
    agent_colors = px.colors.sequential.Plasma
    supervisor_colors = px.colors.sequential.Cividis

    fig = go.Figure()

    if bottom_employees is not None:
        fig.add_trace(go.Bar(
            y=top_employees[employee_type],
            x=top_employees['WeightedAvgCSATScore'] if weight_by_volume else top_employees['AvgCSATScore'],
            orientation='h',
            marker_color=supervisor_colors[2] if employee_type == 'SupervisorName' else agent_colors[2],
            name=f'Top {employee_type}s'
        ))
        fig.add_trace(go.Bar(
            y=bottom_employees[employee_type],
            x=bottom_employees['WeightedAvgCSATScore'] if weight_by_volume else bottom_employees['AvgCSATScore'],
            orientation='h',
            marker_color=supervisor_colors[-3] if employee_type == 'SupervisorName' else agent_colors[-3],
            name=f'Bottom {employee_type}s'
        ))
    else:
        fig.add_trace(go.Bar(
            y=top_employees[employee_type],
            x=top_employees['WeightedAvgCSATScore'] if weight_by_volume else top_employees['AvgCSATScore'],
            orientation='h',
            marker_color=colors,
            name=f'{employee_type}s'
        ))

    fig.update_layout(
        title=f'Top and Bottom {employee_type}s by {"Weighted " if weight_by_volume else ""}CSAT Score',
        xaxis_title='CSAT Score',
        yaxis_title=employee_type,
        yaxis=dict(autorange='reversed'),
        height=max(500, num_employees * 50),
        barmode='group',
        bargap=0.1
    )

    return fig

def mirrored_bar_chart(data):
    employee_type = st.selectbox('Select Employee Type', ['AgentName', 'SupervisorName', 'ManagerName'])
    
    if employee_type == 'ManagerName':
        num_employees = len(data[employee_type].unique())
    else:
        options = [5, 10, 'All'] if employee_type == 'SupervisorName' else [5, 10, 20, 50, 'All']
        num_employees = st.selectbox('Number of Employees', options)
        if num_employees == 'All':
            num_employees = len(data[employee_type].unique())
        else:
            num_employees = int(num_employees)
    
    weight_by_volume = st.checkbox('Weighted Average')
    fig = create_mirrored_bar_chart(data, employee_type, num_employees, weight_by_volume)
    st.plotly_chart(fig, use_container_width=True)

def render_mirrored_bar_chart(data):
    st.markdown("<br>", unsafe_allow_html=True) 
    st.title('Mirrored Bar Chart: Top and Bottom Employees')
    st.write('The weighting option adjusts the rankings based on the interaction volume of each employee.')
    st.markdown("<br>", unsafe_allow_html=True) 
    mirrored_bar_chart(data)