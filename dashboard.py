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

    # Sidebar title and description
    st.sidebar.write('Use the filters below to refine the data displayed in the dashboard.')

    # Date range filter
    date_range = st.sidebar.date_input("Select Date Range", [])
    st.sidebar.title('Filters')

    # Extract unique values from the one-hot encoded columns
    channel_columns = [col.replace('ChannelName_', '') for col in data.columns if col.startswith('ChannelName_')]
    shift_columns = [col.replace('AgentShift_', '') for col in data.columns if col.startswith('AgentShift_') and col != 'AgentShift_nan']
    category_columns = [col.replace('ProductCategory_', '') for col in data.columns if col.startswith('ProductCategory_')]

    # Add "ALL" option to each filter
    channel_columns.insert(0, 'ALL')
    shift_columns.insert(0, 'ALL')
    category_columns.insert(0, 'ALL')
    category_columns.append('No Product Category')

    # Create multiselect widgets for each category
    channel_filter = st.sidebar.multiselect('Channel', options=channel_columns, default=['ALL'])
    shift_filter = st.sidebar.multiselect('Agent Shift', options=shift_columns, default=['ALL'])
    category_filter = st.sidebar.multiselect('Product Category', options=category_columns, default=['ALL'])

    # Apply filters based on user selection
    channel_filter = [f'ChannelName_{ch}' for ch in channel_filter if ch != 'ALL']
    shift_filter = [f'AgentShift_{sh}' for sh in shift_filter if sh != 'ALL']
    category_filter = [f'ProductCategory_{cat}' for cat in category_filter if cat != 'ALL' and cat != 'No Product Category']

    if 'No Product Category' in category_filter:
        data_filtered = data[(data[channel_filter + shift_filter].any(axis=1)) & (data['ProductCategory'].isna() | data[category_filter].any(axis=1))]
    else:
        data_filtered = data[data[channel_filter + shift_filter + category_filter].any(axis=1)]

    # Display the dashboard title and description
    st.title('Customer Satisfaction Analysis Dashboard')
    st.write('This dashboard presents an analysis of customer satisfaction based on the provided dataset.')

    # CSAT Score Distribution
    csat_score_distribution = plot_csat_score_distribution(data_filtered)
    st.plotly_chart(csat_score_distribution, use_container_width=True)

    # Agent Tenure vs CSAT Score
    agent_tenure_vs_csat_score = plot_agent_tenure_vs_csat_score(data_filtered)
    st.plotly_chart(agent_tenure_vs_csat_score, use_container_width=True)

    # Ticket Category vs CSAT Score
    ticket_category_vs_csat_score = plot_ticket_category_vs_csat_score(data_filtered)
    st.plotly_chart(ticket_category_vs_csat_score, use_container_width=True)

    # Response Time vs CSAT Score
    response_time_vs_csat_score = plot_response_time_vs_csat_score(data_filtered)
    st.plotly_chart(response_time_vs_csat_score, use_container_width=True)

    # Customer Remarks Word Cloud
    wordcloud = generate_customer_remarks_wordcloud(data_filtered)
    st.image(wordcloud.to_array(), use_column_width=True)

    # Key Factors Influencing CSAT Scores
    n_features = min(10, data_filtered.shape[1] - 1)  # Ensure n_features is not greater than the number of available features
    rf_top_features, _ = perform_feature_selection(data_filtered, 'CSATScore', n_features)
    top_features_slider = st.slider('Number of Top Features', min_value=5, max_value=len(rf_top_features), value=10, step=1)
    top_features_fig = px.bar(rf_top_features.head(top_features_slider), x='Importance', y='Feature', orientation='h', color='Importance', color_continuous_scale='Viridis')
    top_features_fig.update_layout(title=f'Top {top_features_slider} Factors Influencing CSAT Scores', xaxis_title='Importance', yaxis_title='Feature', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(top_features_fig, use_container_width=True)

    # Decision Tree Visualization and Model Evaluation
    dt_model, rf_model, dt_accuracy, dt_precision, dt_recall, dt_f1, dt_cm_fig, dt_roc_fig, rf_accuracy, rf_precision, rf_recall, rf_f1, rf_cm_fig, rf_roc_fig = train_and_evaluate_models(data_filtered, 'CSATScore')

    # Display Decision Tree Visualization
    st.subheader('Decision Tree Visualization')
    st.pyplot(dtreeviz(dt_model, data_filtered.drop(columns=['CSATScore']), data_filtered['CSATScore'], target_name="CSATScore", feature_names=data_filtered.drop(columns=['CSATScore']).columns, class_names=list(map(str, data_filtered['CSATScore'].unique())), scale=1.5, orientation='LR', fancy=True, histtype='strip'))

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
    insights = generate_insights(data_filtered, rf_top_features)
    st.subheader('Actionable Insights')
    for insight in insights:
        st.text(insight)

    # Handling Missing Data Impact on CSAT Scores
    st.subheader('Impact of Missing Data on CSAT Scores')
    missing_data_impact_fig = plot_missing_data_impact(data_filtered)
    st.plotly_chart(missing_data_impact_fig, use_container_width=True)

if __name__ == '__main__':
    main()
