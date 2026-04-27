import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Machine Learning Imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Energy Intelligence Dashboard",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e9ecef; }
    div[data-testid="stExpander"] { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)


# 2. DATA & MODEL CACHING
@st.cache_resource
def build_model_engine():
    try:
        # Loading your dataset
        df = pd.read_csv("energy_data.csv")

        X = df.drop("Energy Consumption", axis=1)
        y = df["Energy Consumption"]

        # Preprocessing setup
        categorical_features = ["Building Type", "Day of Week"]
        numerical_features = ["Square Footage", "Number of Occupants", "Appliances Used", "Average Temperature"]

        preprocessor = ColumnTransformer([
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

        # Pipeline construction
        model_pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=200, random_state=42))
        ])

        # Training
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model_pipeline.fit(X_train, y_train)

        # Calculate metrics
        y_pred = model_pipeline.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        return model_pipeline, mse, r2, y_test, y_pred, X.columns.tolist()

    except FileNotFoundError:
        return None, None, None, None, None, None


# Initialize Model
model, mse, r2, y_test, y_pred, feat_cols = build_model_engine()

# --- UI START ---
if model is None:
    st.error("🚨 'energy_data.csv' not found! Please ensure the dataset is in the same directory.")
    st.stop()

# SIDEBAR - INPUT CONTROLS
st.sidebar.header("🏢 Input Parameters")
st.sidebar.markdown("Modify the values below to update the prediction.")

with st.sidebar:
    with st.form("prediction_form"):
        b_type = st.selectbox("Building Type", ["Residential", "Commercial", "Industrial"])
        day = st.selectbox("Day of Week", ["Weekday", "Weekend"])
        sq_ft = st.slider("Square Footage", 500, 100000, 30000, step=500)
        occ = st.number_input("Occupants", min_value=1, max_value=1000, value=50)
        apps = st.number_input("Appliances in Use", min_value=1, max_value=200, value=20)
        temp = st.slider("Average Temp (°C)", -10, 50, 25)

        submit_button = st.form_submit_button(label="Calculate Prediction")

# MAIN DASHBOARD AREA
st.title("⚡ Energy Consumption Predictive Analytics")
st.markdown("This dashboard uses a **Random Forest Regressor** to estimate energy demand based on facility metadata.")

# TOP METRICS ROW
col1, col2, col3 = st.columns(3)

# Prepare input for prediction
new_input = pd.DataFrame([[b_type, sq_ft, occ, apps, temp, day]],
                         columns=["Building Type", "Square Footage", "Number of Occupants",
                                  "Appliances Used", "Average Temperature", "Day of Week"])
current_pred = model.predict(new_input)[0]

with col1:
    st.metric(label="Estimated Consumption", value=f"{current_pred:.2f} kWh")

with col2:
    st.metric(label="Model R² Score", value=f"{r2:.4f}",
              help="Indicates how well the model explains the variance (Max 1.0)")

with col3:
    st.metric(label="Mean Squared Error", value=f"{mse:.2f}")

st.divider()

# VISUALIZATION ROW
left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("Model Performance (Actual vs Predicted)")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x=y_test, y=y_pred, scatter_kws={'alpha': 0.5, 'color': '#2c3e50'}, line_kws={'color': '#e74c3c'})
    plt.xlabel("Actual Energy (kWh)")
    plt.ylabel("Predicted Energy (kWh)")
    st.pyplot(fig)

with right_chart:
    st.subheader("Feature Importance")
    # Extract feature importance
    importances = model.named_steps['regressor'].feature_importances_
    # Note: OHE creates extra columns, but for simplicity, we map back to main categories
    # or show the processed feature names
    ohe_cols = model.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out()
    all_feat_names = ["Sq Ft", "Occupants", "Appliances", "Temp"] + list(ohe_cols)

    feat_importances = pd.Series(importances, index=all_feat_names).sort_values(ascending=True)

    fig_imp, ax_imp = plt.subplots(figsize=(10, 6))
    feat_importances.tail(10).plot(kind='barh', color='#3498db', ax=ax_imp)
    plt.title("Top Impact Factors")
    st.pyplot(fig_imp)

# BOTTOM DATA VIEW
with st.expander("🔍 View Raw Prediction Data"):
    st.write("Below is the data frame sent to the model engine:")
    st.dataframe(new_input, use_container_width=True)

st.caption("Developed with Scikit-Learn and Streamlit | v1.2")