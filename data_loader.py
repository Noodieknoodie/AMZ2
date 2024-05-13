import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

@st.cache_data
def preprocess_data(data):
    # Fill missing values for text and categoricals with a placeholder
    data['CustomerRemarks'].fillna('No Remarks', inplace=True)
    data['ProductCategory'].fillna('Unknown', inplace=True)
    
    # Convert date columns and handle missing dates
    date_columns = ['OrderDateTime', 'SurveyResponseDate']  # Removed 'IssueReportedDateTime' and 'IssueRespondedDateTime'
    for column in date_columns:
        data[column] = pd.to_datetime(data[column], errors='coerce')
    data['OrderDateTime'].fillna(method='ffill', inplace=True)  # Forward fill for missing dates, if appropriate
    
    # Handle numeric data
    data['ResponseTimeMinutes'] = pd.to_numeric(data['ResponseTimeMinutes'], errors='coerce')
    data['ResponseTimeMinutes'].fillna('ERROR', inplace=True)  # Use 'ERROR' for missing response times
    
    # Create new boolean features
    data['HasCustomerRemarks'] = data['CustomerRemarks'].notna()
    data['HasProductCategory'] = data['ProductCategory'].notna()
    data['HasResponseTime'] = data['ResponseTimeMinutes'].notna()
    
    # One-hot encoding for categorical columns
    categorical_columns = [
        'ChannelName', 'TicketCategory', 'TicketSubCategory', 'AgentName',
        'SupervisorName', 'ManagerName', 'AgentTenure', 'AgentShift', 'ProductCategory', 'ResponseTimeMinutes'  # Added 'ResponseTimeMinutes'
    ]
    data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)
    
    return data

@st.cache_data
def load_and_preprocess_data():
    file_path = 'data/RawAmazonData.csv'
    data = load_data(file_path)
    preprocessed_data = preprocess_data(data)
    return preprocessed_data