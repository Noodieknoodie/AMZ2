# feature_selection.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, chi2

def select_features_with_random_forest(data, target_column, n_features):
    X = data.drop(columns=[target_column]).select_dtypes(include=[int, float])
    y = data[target_column]
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    feature_importances = rf.feature_importances_
    feature_names = X.columns
    feature_importances_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
    top_features = feature_importances_df.nlargest(n_features, 'Importance')
    return top_features

def select_features_with_chi2(data, target_column, n_features):
    X = data.drop(columns=[target_column]).select_dtypes(include=[int, float])
    y = data[target_column]
    n_features = min(n_features, X.shape[1])  # Ensure n_features is not greater than the number of available features
    selector = SelectKBest(chi2, k=n_features)
    selector.fit(X, y)
    feature_scores = selector.scores_
    feature_names = X.columns
    feature_scores_df = pd.DataFrame({'Feature': feature_names, 'Score': feature_scores})
    top_features = feature_scores_df.nlargest(n_features, 'Score')
    return top_features

def perform_feature_selection(data, target_column, n_features):
    rf_top_features = select_features_with_random_forest(data, target_column, n_features)
    chi2_top_features = select_features_with_chi2(data, target_column, n_features)
    return rf_top_features, chi2_top_features