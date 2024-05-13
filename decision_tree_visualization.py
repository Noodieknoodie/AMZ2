## This file is commented out becasue it was moved into the dashboard.py file due to an updated way of rendering the decision tree visualization. (i think?)

""" # decision_tree_visualization.py
from dtreeviz import dtreeviz 
import streamlit.components.v1 as components

def interactive_decision_tree_viz(model, X_train, y_train, feature_names, class_names, tree_depth=3):
    viz = dtreeviz(model, X_train, y_train, target_name="CSATScore",
                   feature_names=feature_names, class_names=list(map(str, class_names)),
                   tree_depth=tree_depth, orient='LR', fancy=True, histtype='strip')
    return viz.svg()

def generate_decision_tree_visualizations(model, X_train, y_train, feature_names, class_names):
    interactive_html = interactive_decision_tree_viz(model, X_train, y_train, feature_names, class_names)
    return interactive_html
 """