import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud

def plot_csat_score_distribution(data):
    csat_counts = data['CSATScore'].value_counts(normalize=True).reset_index()
    csat_counts.columns = ['CSATScore', 'percentage']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    fig = px.bar(csat_counts, x='CSATScore', y='percentage', color='CSATScore',
                 color_discrete_sequence=colors, text='percentage')
    fig.update_traces(texttemplate='%{text:.1%}', textposition='outside')
    fig.update_layout(title='CSAT Score Distribution', xaxis_title='CSAT Score', yaxis_title='Percentage',
                      legend_title_text='CSAT Score', yaxis_range=[0, csat_counts['percentage'].max() * 1.1])
    return fig

def plot_agent_tenure_vs_csat_score(data):
    tenure_order = ['On Job Training', '0-30', '31-60', '61-90', '>90']
    tenure_csat = data.groupby('AgentTenure', observed=True)['CSATScore'].mean().reindex(tenure_order).reset_index()
    fig = px.bar(tenure_csat, x='AgentTenure', y='CSATScore', color_discrete_sequence=['#1f77b4'], text='CSATScore')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(title='Agent Tenure vs CSAT Score', xaxis_title='Agent Tenure', yaxis_title='Average CSAT Score',
                      xaxis={'categoryorder': 'array', 'categoryarray': tenure_order},
                      yaxis_range=[tenure_csat['CSATScore'].min() * 0.9, tenure_csat['CSATScore'].max() * 1.05])
    return fig

def plot_product_category_vs_csat_score(data):
    product_csat = data.groupby('ProductCategory', observed=True)['CSATScore'].mean().reset_index()
    product_csat = product_csat.sort_values('CSATScore', ascending=False)
    fig = px.bar(product_csat, y='ProductCategory', x='CSATScore', color_discrete_sequence=['#2ca02c'],
                 orientation='h', text='CSATScore')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(title='Average CSAT Score by Product Category', xaxis_title='Average CSAT Score',
                      yaxis_title='Product Category',
                      xaxis_range=[product_csat['CSATScore'].min() * 0.9, product_csat['CSATScore'].max() * 1.05])
    return fig

def plot_response_time_vs_csat_score(data):
    data_copy = data.copy()
    data_copy.loc[:, 'ResponseTimeBucket'] = pd.cut(data_copy['ResponseTimeMinutes'], bins=[0, 15, 30, 60, float('inf')], 
                                                    labels=['0-15', '15-30', '30-60', '60+'], include_lowest=True)
    response_csat = data_copy.groupby('ResponseTimeBucket', observed=True)['CSATScore'].mean().reset_index()
    fig = px.line(response_csat, x='ResponseTimeBucket', y='CSATScore', markers=True, color_discrete_sequence=['#9467bd'],
                  labels={'ResponseTimeBucket': 'Response Time (Minutes)', 'CSATScore': 'Average CSAT Score'})
    fig.update_layout(title='Response Time vs CSAT Score', xaxis_title='Response Time (Minutes)',
                      yaxis_title='Average CSAT Score',
                      yaxis_range=[response_csat['CSATScore'].min() * 0.9, response_csat['CSATScore'].max() * 1.05])
    return fig

def generate_customer_remarks_wordcloud(data):
    text = ' '.join(data['CustomerRemarks'].fillna('').astype(str))
    text = text.replace("No Remark", "")
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Blues').generate(text)
    return wordcloud

def plot_missing_data_impact(data):
    placeholders = {
        'ProductCategory': 'No Product Category',
        'AgentShift': 'No Agent Shift'
    }
    missing_data_columns = ['CustomerRemarks', 'ResponseTimeMinutes', 'ProductCategory']
    fig = make_subplots(rows=1, cols=len(missing_data_columns), subplot_titles=missing_data_columns, shared_yaxes=True)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    y_min = float('inf')
    y_max = float('-inf')
    for i, column in enumerate(missing_data_columns):
        data_copy = data.copy()
        if column in placeholders:
            data_copy.loc[:, 'Has' + column] = ~data_copy[column].isin([placeholders[column]])
        else:
            data_copy.loc[:, 'Has' + column] = data_copy[column].notnull()
        impact_df = data_copy.groupby('Has' + column, observed=True)['CSATScore'].mean().reset_index()
        impact_df['count'] = data_copy.groupby('Has' + column).size().reset_index(name='count')['count']
        impact_df['Has' + column] = impact_df['Has' + column].map({True: 'Present', False: 'Missing'})
        y_min = min(y_min, impact_df['CSATScore'].min())
        y_max = max(y_max, impact_df['CSATScore'].max())
        fig.add_trace(
            go.Bar(x=impact_df['Has' + column], y=impact_df['CSATScore'], text=impact_df['CSATScore'],
                   texttemplate='%{text:.2f}', textposition='outside', name=column, marker_color=colors[i]),
            row=1, col=i+1
        )
    fig.update_yaxes(range=[y_min * 0.9, y_max * 1.05])
    fig.update_layout(
        title='Impact of Missing Data on CSAT Scores',
        xaxis_title='Data Completeness',
        yaxis_title='Average CSAT Score',
        showlegend=True,
        legend_title_text='Data Field'
    )
    return fig