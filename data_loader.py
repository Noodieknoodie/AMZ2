import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

@st.cache_data
def preprocess_data(data):
    # Create new boolean features for missing values
    data['HasCustomerRemarks'] = data['CustomerRemarks'].notna()
    data['CustomerRemarks'].fillna('', inplace=True)  # Replace missing values with an empty string
    
    data['HasProductCategory'] = data['ProductCategory'].notna()
    data['ProductCategory'].fillna('Unknown', inplace=True)  # Keep 'Unknown' category
    
    data['HasResponseTime'] = data['ResponseTimeMinutes'] != 'ERROR'
    data['ResponseTimeMinutes'] = pd.to_numeric(data['ResponseTimeMinutes'], errors='coerce')  # Convert 'ERROR' to NaN
    
    # Convert date columns and handle missing dates
    date_columns = ['OrderDateTime', 'SurveyResponseDate']
    for column in date_columns:
        data[column] = pd.to_datetime(data[column], errors='coerce')
    data['OrderDateTime'].fillna(method='ffill', inplace=True)
    
    # One-hot encoding for categorical columns
    categorical_columns = [
        'ChannelName', 'TicketCategory', 'TicketSubCategory', 'AgentName',
        'SupervisorName', 'ManagerName', 'AgentTenure', 'AgentShift', 'ProductCategory'
    ]
    data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)
    
    return data

@st.cache_data
def load_and_preprocess_data():
    file_path = 'data/RawAmazonData.csv'
    data = load_data(file_path)
    preprocessed_data = preprocess_data(data)
    return preprocessed_data