# feature_selection.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif

def select_features_with_random_forest(data, target_column, n_features):
    X = data.drop(columns=[target_column])
    y = data[target_column]
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    feature_importances = rf.feature_importances_
    feature_names = X.columns
    feature_importances_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
    top_features = feature_importances_df.nlargest(n_features, 'Importance')
    return top_features

def select_features_with_f_score(data, target_column, n_features):
    X = data.drop(columns=[target_column])
    y = data[target_column]
    selector = SelectKBest(f_classif, k=n_features)
    selector.fit(X, y)
    feature_scores = selector.scores_
    feature_names = X.columns
    feature_scores_df = pd.DataFrame({'Feature': feature_names, 'Score': feature_scores})
    top_features = feature_scores_df.nlargest(n_features, 'Score')
    return top_features

def perform_feature_selection(data, target_column, n_features):
    rf_top_features = select_features_with_random_forest(data, target_column, n_features)
    f_score_top_features = select_features_with_f_score(data, target_column, n_features)
    return rf_top_features, f_score_top_features