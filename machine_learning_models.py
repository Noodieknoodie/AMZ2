# machine_learning_models.py
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
import plotly.graph_objects as go
import plotly.figure_factory as ff

def split_data(data, target_column, test_size=0.2, random_state=42):
    X = data.drop(columns=[target_column])
    y = data[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def train_decision_tree(X_train, y_train, max_depth=5, random_state=42):
    dt = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
    dt.fit(X_train, y_train)
    return dt

def train_random_forest(X_train, y_train, n_estimators=100, max_depth=5, random_state=42):
    rf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
    rf.fit(X_train, y_train)
    return rf

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred)
    fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
    roc_auc = auc(fpr, tpr)
    return accuracy, precision, recall, f1, cm, fpr, tpr, roc_auc

def plot_confusion_matrix(cm, labels):
    fig = ff.create_annotated_heatmap(cm, x=labels, y=labels, colorscale='Viridis')
    fig.update_layout(title='Confusion Matrix', xaxis_title='Predicted', yaxis_title='Actual')
    return fig

def plot_roc_curve(fpr, tpr, roc_auc, model_name):
    fig = go.Figure(data=go.Scatter(x=fpr, y=tpr, mode='lines', name=model_name))
    fig.add_shape(type='line', line=dict(dash='dash'), x0=0, x1=1, y0=0, y1=1)
    fig.update_layout(title=f'ROC Curve (AUC = {roc_auc:.2f})', xaxis_title='False Positive Rate', yaxis_title='True Positive Rate')
    return fig

def train_and_evaluate_models(data, target_column):
    X_train, X_test, y_train, y_test = split_data(data, target_column)
    dt_model = train_decision_tree(X_train, y_train)
    rf_model = train_random_forest(X_train, y_train)
    dt_accuracy, dt_precision, dt_recall, dt_f1, dt_cm, dt_fpr, dt_tpr, dt_roc_auc = evaluate_model(dt_model, X_test, y_test)
    rf_accuracy, rf_precision, rf_recall, rf_f1, rf_cm, rf_fpr, rf_tpr, rf_roc_auc = evaluate_model(rf_model, X_test, y_test)
    dt_cm_fig = plot_confusion_matrix(dt_cm, labels=list(data[target_column].unique()))
    rf_cm_fig = plot_confusion_matrix(rf_cm, labels=list(data[target_column].unique()))
    dt_roc_fig = plot_roc_curve(dt_fpr, dt_tpr, dt_roc_auc, 'Decision Tree')
    rf_roc_fig = plot_roc_curve(rf_fpr, rf_tpr, rf_roc_auc, 'Random Forest')
    return dt_model, rf_model, dt_accuracy, dt_precision, dt_recall, dt_f1, dt_cm_fig, dt_roc_fig, rf_accuracy, rf_precision, rf_recall, rf_f1, rf_cm_fig, rf_roc_fig