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
    ticket_category_columns = [col for col in data.columns if col.startswith('TicketCategory_')]
    ticket_subcategory_columns = [col for col in data.columns if col.startswith('TicketSubCategory_')]
    pivot_data = data.groupby(ticket_subcategory_columns)[['CSATScore'] + ticket_category_columns].mean()
    fig = go.Figure(data=go.Heatmap(z=pivot_data.values, x=ticket_category_columns, y=pivot_data.index, colorscale='RdYlGn'))
    fig.update_layout(title='Ticket Category vs CSAT Score', xaxis_title='Ticket Category', yaxis_title='Ticket Subcategory')
    return fig

def plot_response_time_vs_csat_score(data):
    fig = px.scatter(data, x='ResponseTimeMinutes', y='CSATScore', 
                     color='CSATScore', color_continuous_scale='Bluered',
                     labels={'ResponseTimeMinutes': 'Response Time (Minutes)', 'CSATScore': 'CSAT Score'})
    fig.update_layout(title='Response Time vs CSAT Score')
    return fig

def generate_customer_remarks_wordcloud(data):
    text = ' '.join(data['CustomerRemarks'].fillna('').astype(str))
    text = text.replace("No Remark", "")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

def plot_missing_data_impact(data):
    impact_df = data.groupby(['HasCustomerRemarks', 'HasResponseTime', 'HasProductCategory']).agg({'CSATScore': 'mean'}).reset_index()
    impact_df['Data Completeness'] = impact_df.apply(lambda row: f"Remarks: {'Yes' if row['HasCustomerRemarks'] else 'No'}, Response Time: {'Yes' if row['HasResponseTime'] else 'No'}, Product Category: {'Yes' if row['HasProductCategory'] else 'No'}", axis=1)
    fig = px.bar(impact_df, x='Data Completeness', y='CSATScore', title='Impact of Missing Data on CSAT Scores', labels={'CSATScore': 'Average CSAT Score'})
    return fig