# exploratory_data_analysis.py
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

def plot_csat_score_distribution(data):
    fig = px.bar(data['CSATScore'].value_counts().reset_index(), x='index', y='CSATScore', color='index', color_discrete_sequence=['#FF4136', '#FFDC00', '#2ECC40'])
    fig.update_layout(title='CSAT Score Distribution', xaxis_title='CSAT Score', yaxis_title='Count')
    return fig

def plot_agent_tenure_vs_csat_score(data):
    fig = px.bar(data.groupby('AgentTenure', as_index=False).agg({'CSATScore': 'mean', 'AgentName': 'count'}), x='AgentTenure', y='CSATScore', hover_data=['AgentName'], color='CSATScore', color_continuous_scale='Viridis')
    fig.update_layout(title='Agent Tenure vs CSAT Score', xaxis_title='Agent Tenure', yaxis_title='Average CSAT Score')
    return fig

def plot_ticket_category_vs_csat_score(data):
    pivot_data = data.pivot_table(index='TicketSubCategory', columns='TicketCategory', values='CSATScore', aggfunc='mean')
    fig = go.Figure(data=go.Heatmap(z=pivot_data.values, x=pivot_data.columns, y=pivot_data.index, colorscale='RdYlGn'))
    fig.update_layout(title='Ticket Category vs CSAT Score', xaxis_title='Ticket Category', yaxis_title='Ticket Subcategory')
    return fig

def generate_customer_remarks_wordcloud(data):
    text = ' '.join(data['CustomerRemarks'].fillna('').astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud