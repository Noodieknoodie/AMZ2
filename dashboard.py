# dashboard.py
import streamlit as st
from dtreeviz import dtreeviz
import plotly.express as px
from data_loader import load_and_preprocess_data
from exploratory_data_analysis import (
    plot_csat_score_distribution, 
    plot_agent_tenure_vs_csat_score, 
    plot_ticket_category_vs_csat_score, 
    plot_response_time_vs_csat_score, 
    generate_customer_remarks_wordcloud, 
    plot_missing_data_impact
)
from feature_selection import perform_feature_selection
from machine_learning_models import train_and_evaluate_models
from insights_generator import generate_insights

def main():
    st.set_page_config(page_title='Customer Satisfaction Analysis Dashboard', layout='wide')
    # Load CSS
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    # Load and preprocess data
    data = load_and_preprocess_data()
    # Sidebar filters using direct category selection, properly handling 'All' cases
    st.sidebar.title('Filters')
    # Extract unique values directly from the data columns
    channel_options = ['All'] + sorted(data['ChannelName'].dropna().unique().tolist())
    shift_options = ['All'] + sorted(data['AgentShift'].dropna().unique().tolist())
    category_options = ['All', 'None'] + sorted(data['ProductCategory'].dropna().unique().tolist())
    # Use these options for the multiselect widgets
    channel_filter = st.sidebar.multiselect('Channel', options=channel_options, default=['All'])
    shift_filter = st.sidebar.multiselect('Agent Shift', options=shift_options, default=['All'])
    category_filter = st.sidebar.multiselect('Product Category', options=category_options, default=['All'])
    # Apply filters based on user selection
    if 'All' not in channel_filter:
        data = data[data['ChannelName'].isin(channel_filter)]
    if 'All' not in shift_filter:
        data = data[data['AgentShift'].isin(shift_filter)]
    if 'All' not in category_filter:
        if 'None' in category_filter:
            if len(category_filter) == 1:
                data = data[data['ProductCategory'].isna()]
            else:
                selected_categories = [cat for cat in category_filter if cat != 'None']
                data = data[data['ProductCategory'].isna() | data['ProductCategory'].isin(selected_categories)]
        else:
            data = data[data['ProductCategory'].isin(category_filter)]
    # Display the dashboard title and description
    st.title('Customer Satisfaction Analysis Dashboard')
    st.write('This dashboard presents an analysis of customer satisfaction based on the provided dataset.')
    # CSAT Score Distribution
    csat_score_distribution = plot_csat_score_distribution(data)
    st.plotly_chart(csat_score_distribution, use_container_width=True)
    # Agent Tenure vs CSAT Score
    agent_tenure_vs_csat_score = plot_agent_tenure_vs_csat_score(data)
    st.plotly_chart(agent_tenure_vs_csat_score, use_container_width=True)
    # Ticket Category vs CSAT Score
    ticket_category_vs_csat_score = plot_ticket_category_vs_csat_score(data)
    st.plotly_chart(ticket_category_vs_csat_score, use_container_width=True)
    # Response Time vs CSAT Score
    response_time_vs_csat_score = plot_response_time_vs_csat_score(data)
    st.plotly_chart(response_time_vs_csat_score, use_container_width=True)
    # Customer Remarks Word Cloud
    wordcloud = generate_customer_remarks_wordcloud(data)
    st.image(wordcloud.to_array(), use_column_width=True)
    # Key Factors Influencing CSAT Scores
    n_features = min(10, data.shape[1] - 1)  # Ensure n_features is not greater than the number of available features
    rf_top_features, _ = perform_feature_selection(data, 'CSATScore', n_features)
    top_features_slider = st.slider('Number of Top Features', min_value=5, max_value=len(rf_top_features), value=10, step=1)
    top_features_fig = px.bar(rf_top_features.head(top_features_slider), x='Importance', y='Feature', orientation='h', color='Importance', color_continuous_scale='Viridis')
    top_features_fig.update_layout(title=f'Top {top_features_slider} Factors Influencing CSAT Scores', xaxis_title='Importance', yaxis_title='Feature', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(top_features_fig, use_container_width=True)
    # Decision Tree Visualization and Model Evaluation
    dt_model, rf_model, dt_accuracy, dt_precision, dt_recall, dt_f1, dt_cm_fig, dt_roc_fig, rf_accuracy, rf_precision, rf_recall, rf_f1, rf_cm_fig, rf_roc_fig = train_and_evaluate_models(data, 'CSATScore')
    # Display Decision Tree Visualization
    st.subheader('Decision Tree Visualization')
    st.pyplot(dtreeviz(dt_model, data.drop(columns=['CSATScore']), data['CSATScore'], target_name="CSATScore", feature_names=data.drop(columns=['CSATScore']).columns, class_names=list(map(str, data['CSATScore'].unique())), scale=1.5, orientation='LR', fancy=True, histtype='strip'))
    # Model Evaluation Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Decision Tree Metrics')
        st.write(f'Accuracy: {dt_accuracy:.2f}')
        st.write(f'Precision: {dt_precision:.2f}')
        st.write(f'Recall: {dt_recall:.2f}')
        st.write(f'F1 Score: {dt_f1:.2f}')
        st.plotly_chart(dt_cm_fig, use_container_width=True)
        st.plotly_chart(dt_roc_fig, use_container_width=True)
    with col2:
        st.subheader('Random Forest Metrics')
        st.write(f'Accuracy: {rf_accuracy:.2f}')
        st.write(f'Precision: {rf_precision:.2f}')
        st.write(f'Recall: {rf_recall:.2f}')
        st.write(f'F1 Score: {rf_f1:.2f}')
        st.plotly_chart(rf_cm_fig, use_container_width=True)
        st.plotly_chart(rf_roc_fig, use_container_width=True)
    # Actionable Insights
    insights = generate_insights(data, rf_top_features)
    st.subheader('Actionable Insights')
    for insight in insights:
        st.text(insight)
    # Handling Missing Data Impact on CSAT Scores
    st.subheader('Impact of Missing Data on CSAT Scores')
    missing_data_impact_fig = plot_missing_data_impact(data)
    st.plotly_chart(missing_data_impact_fig, use_container_width=True)

if __name__ == '__main__':
    main()