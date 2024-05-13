#data_loader.py
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path):
    # Assuming blanks are represented by empty strings in the CSV
    data = pd.read_csv(file_path, na_values=['', ' '])
    return data

@st.cache_data
def preprocess_data(data):
    # Create indicators for missing data
    data['HasCustomerRemarks'] = data['CustomerRemarks'].notna()
    data['HasResponseTime'] = data['ResponseTimeMinutes'].notna()
    data['HasProductCategory'] = data['ProductCategory'].notna()
    
    # Selecting features for one-hot encoding
    categorical_features = ['TicketCategory', 'TicketSubCategory', 'ManagerName', 'SupervisorName']
    # Apply one-hot encoding to the selected features
    data = pd.concat([data, pd.get_dummies(data[categorical_features], prefix=categorical_features, dummy_na=True)], axis=1)
    data.drop(columns=categorical_features, inplace=True)
    
    # Retain 'ChannelName', 'AgentShift', 'ProductCategory' for filtering
    return data

@st.cache_data
def load_and_preprocess_data():
    file_path = 'data/RawAmazonData.csv'
    data = load_data(file_path)
    preprocessed_data = preprocess_data(data)
    return preprocessed_data
