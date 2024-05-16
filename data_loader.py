import pandas as pd
import streamlit as st
from sklearn.impute import SimpleImputer

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path, na_values=['', ' '])
    return data

@st.cache_data
def preprocess_data(data):
    # Indicators for missing data
    data['HasCustomerRemarks'] = data['CustomerRemarks'].notna()
    data['HasResponseTime'] = data['ResponseTimeMinutes'].notna()
    data['HasProductCategory'] = data['ProductCategory'].notna()
    
    # Convert ResponseTimeMinutes to numeric, coercing errors to NaN
    data['ResponseTimeMinutes'] = pd.to_numeric(data['ResponseTimeMinutes'], errors='coerce')
    
    # Categorical features for one-hot encoding, exclude features used in front-end filters
    categorical_features = ['TicketCategory', 'TicketSubCategory', 'ManagerName', 'SupervisorName']
    data_encoded = pd.get_dummies(data[categorical_features], prefix=categorical_features, dummy_na=True)
    data.drop(columns=categorical_features, inplace=True)
    data = pd.concat([data, data_encoded], axis=1)
    
    # Impute missing numeric values
    numeric_features = data.select_dtypes(include=[float, int]).columns
    imputer = SimpleImputer(strategy='mean')
    data[numeric_features] = imputer.fit_transform(data[numeric_features])
    
    return data

@st.cache_data
def load_and_preprocess_data():
    file_path = 'data/RawAmazonData.csv'
    data = load_data(file_path)
    preprocessed_data = preprocess_data(data)
    return preprocessed_data
