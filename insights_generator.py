# insights_generator.py
import pandas as pd
import streamlit as st

def get_top_features(feature_importance_df, n=5):
    top_features = feature_importance_df.nlargest(n, 'Importance')
    return top_features

def get_agent_tenure_with_highest_csat(data):
    agent_tenure_csat = data.groupby('AgentTenure')['CSATScore'].mean().reset_index()
    highest_csat_tenure = agent_tenure_csat.loc[agent_tenure_csat['CSATScore'].idxmax(), 'AgentTenure']
    return highest_csat_tenure

def get_ticket_category_subcategory_with_lowest_csat(data, n=3):
    ticket_csat = data.groupby(['TicketCategory', 'TicketSubCategory'])['CSATScore'].mean().reset_index()
    lowest_csat_tickets = ticket_csat.nsmallest(n, 'CSATScore')
    return lowest_csat_tickets

def generate_insights(data, feature_importance_df):
    top_features = get_top_features(feature_importance_df)
    highest_csat_tenure = get_agent_tenure_with_highest_csat(data)
    lowest_csat_tickets = get_ticket_category_subcategory_with_lowest_csat(data)

    with st.expander("Actionable Insights"):
        st.markdown(f"**Top 5 Features Influencing CSAT Scores:**")
        for feature, importance in zip(top_features['Feature'], top_features['Importance']):
            st.markdown(f"- {feature} (Importance: {importance:.2f})")
        
        st.markdown(f"**AgentTenure Category with Highest Average CSAT Score:**")
        st.markdown(f"- {highest_csat_tenure}")
        
        st.markdown(f"**Top 3 TicketCategory and TicketSubCategory Combinations with Lowest Average CSAT Scores:**")
        for _, row in lowest_csat_tickets.iterrows():
            st.markdown(f"- {row['TicketCategory']} - {row['TicketSubCategory']} (Average CSAT Score: {row['CSATScore']:.2f})")

    return top_features, highest_csat_tenure, lowest_csat_tickets