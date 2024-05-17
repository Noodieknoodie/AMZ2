# exploratory_data_analysis_2.py
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from wordcloud import WordCloud



def plot_csat_score_distribution(data):
    csat_counts = data['CSATScore'].value_counts().reset_index()
    csat_counts.columns = ['CSATScore', 'count']
    fig = px.bar(csat_counts, x='CSATScore', y='count', color='CSATScore', 
                 color_discrete_sequence=['#FF4136', '#FFDC00', '#2ECC40'])
    fig.update_layout(title='CSAT Score Distribution', xaxis_title='CSAT Score', yaxis_title='Count')
    return fig

def plot_agent_tenure_vs_csat_score(data):
    tenure_csat = data.groupby('AgentTenure')['CSATScore'].mean().reset_index()
    fig = px.bar(tenure_csat, x='AgentTenure', y='CSATScore', color='CSATScore', 
                 color_continuous_scale='Viridis', text='CSATScore')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(title='Agent Tenure vs CSAT Score', xaxis_title='Agent Tenure', yaxis_title='Average CSAT Score')
    return fig

def plot_product_category_vs_csat_score(data):
    product_csat = data.groupby('ProductCategory')['CSATScore'].mean().reset_index()
    fig = px.bar(product_csat, x='ProductCategory', y='CSATScore', color='CSATScore',
                 title='Average CSAT Score by Product Category')
    return fig

def plot_response_time_vs_csat_score(data):
    fig = px.scatter(data, x='ResponseTimeMinutes', y='CSATScore', color='CSATScore',
                     color_continuous_scale='Bluered', labels={'ResponseTimeMinutes': 'Response Time (Minutes)', 'CSATScore': 'CSAT Score'})
    fig.update_layout(title='Response Time vs CSAT Score')
    return fig

def generate_customer_remarks_wordcloud(data):
    text = ' '.join(data['CustomerRemarks'].fillna('').astype(str))
    text = text.replace("No Remark", "")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

def plot_missing_data_impact(data):
    placeholders = {
        'ProductCategory': 'No Product Category',
        'AgentShift': 'No Agent Shift'
    }
    
    missing_data_columns = ['CustomerRemarks', 'ResponseTimeMinutes', 'ProductCategory']
    
    fig = make_subplots(rows=1, cols=len(missing_data_columns), subplot_titles=missing_data_columns)

    for i, column in enumerate(missing_data_columns):
        if column in placeholders:
            data['Has' + column] = ~data[column].isin([placeholders[column]])
        else:
            data['Has' + column] = data[column].notnull()
        
        impact_df = data.groupby('Has' + column).agg({'CSATScore': 'mean'}).reset_index()
        impact_df['count'] = data.groupby('Has' + column).size().reset_index(name='count')['count']
        impact_df['Has' + column] = impact_df['Has' + column].map({True: 'Present', False: 'Missing'})
        
        fig.add_trace(
            go.Bar(x=impact_df['Has' + column], y=impact_df['CSATScore'], text=impact_df['count'], textposition='auto', name=column),
            row=1, col=i+1
        )

    fig.update_layout(
        title='Impact of Missing Data on CSAT Scores',
        xaxis_title='Data Completeness',
        yaxis_title='Average CSAT Score',
        showlegend=False
    )
    
    return fig