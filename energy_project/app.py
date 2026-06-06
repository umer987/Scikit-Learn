import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


st.set_page_config(
    page_title="Energy Dashboard",
    page_icon="⚡",
    layout="wide"
)

# quick styling fix — default streamlit looks rough
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #fff; padding: 20px; border-radius: 10px; border: 1px solid #e9ecef; }
    div[data-testid="stExpander"] { background-color: white; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)


# cache this so we don't retrain every time a slider moves
@st.cache_resource
def load_and_train():
    try:
        df = pd.read_csv("energy_data.csv")
    except FileNotFoundError:
        return None, None, None, None, None, None

    X = df.drop("Energy Consumption", axis=1)
    y = df["Energy Consumption"]

    cat_cols = ["Building Type", "Day of Week"]
    num_cols = ["Square Footage", "Number of Occupants", "Appliances Used", "Average Temperature"]

    # standard pipeline — scale numerics, OHE the categoricals
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
    ])

    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=200, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe.fit(X_train, y_train)

    preds = pipe.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    return pipe, mse, r2, y_test, preds, X.columns.tolist()


model, mse, r2, y_test, y_pred, feat_cols = load_and_train()

if model is None:
    st.error("Couldn't find energy_data.csv — make sure it's in the same folder as this script.")
    st.stop()


# ---- sidebar inputs ----
st.sidebar.header("🏢 Building Parameters")
st.sidebar.caption("Tweak values and hit Calculate to update the prediction.")

with st.sidebar:
    with st.form("inputs"):
        btype = st.selectbox("Building Type", ["Residential", "Commercial", "Industrial"])
        dow   = st.selectbox("Day of Week", ["Weekday", "Weekend"])
        sqft  = st.slider("Square Footage", 500, 100_000, 30_000, step=500)
        occ   = st.number_input("Occupants", min_value=1, max_value=1000, value=50)
        apps  = st.number_input("Appliances in Use", min_value=1, max_value=200, value=20)
        temp  = st.slider("Avg Temp (°C)", -10, 50, 25)
        go    = st.form_submit_button("Calculate Prediction")


# ---- main area ----
st.title("⚡ Energy Consumption Dashboard")
st.markdown("RF-based prediction model for estimating energy demand. Trained on historical facility data.")

st.markdown("""
<style>
.team-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.team-table th { background-color: #2c3e50; color: white; padding: 10px 16px; text-align: left; font-size: 14px; }
.team-table td { padding: 9px 16px; border-bottom: 1px solid #e9ecef; font-size: 14px; }
.team-table tr:last-child td { border-bottom: none; }
.team-table tr:hover td { background-color: #f1f3f5; }
</style>

<table class="team-table">
  <tr>
    <th colspan="2">Instructor: Sir Dilbar Hussain<br><br>Group Members:</th>
  </tr>
  <tr><td>SYED MUHAMMAD UMER</td><td>62993</td></tr>
  <tr><td>MUHAMMAD SHAH MIR IQBAL</td><td>62602</td></tr>
  <tr><td>MUHAMMAD RAMEEL KHAN</td><td>62780</td></tr>
  <tr><td>WAHADAT MUHAMMAD ASKARI</td><td>63327</td></tr>
</table>
""", unsafe_allow_html=True)

st.divider()

# build the input row from sidebar values
input_row = pd.DataFrame(
    [[btype, sqft, occ, apps, temp, dow]],
    columns=["Building Type", "Square Footage", "Number of Occupants",
             "Appliances Used", "Average Temperature", "Day of Week"]
)
prediction = model.predict(input_row)[0]

# top-line numbers
c1, c2, c3 = st.columns(3)
c1.metric("Predicted Consumption", f"{prediction:.2f} kWh")
c2.metric("R² Score", f"{r2:.4f}", help="How well the model fits (1.0 = perfect)")
c3.metric("MSE", f"{mse:.2f}")

st.divider()

# charts side by side
left, right = st.columns(2)

with left:
    st.subheader("Actual vs Predicted")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(
        x=y_test, y=y_pred,
        scatter_kws={"alpha": 0.5, "color": "#2c3e50"},
        line_kws={"color": "#e74c3c"},
        ax=ax
    )
    ax.set_xlabel("Actual (kWh)")
    ax.set_ylabel("Predicted (kWh)")
    st.pyplot(fig)

with right:
    st.subheader("Feature Importance")

    # need to reconstruct names post-OHE since sklearn expands them
    ohe_names = model.named_steps["preprocessor"] \
                     .named_transformers_["cat"] \
                     .get_feature_names_out()
    all_names = ["Sq Ft", "Occupants", "Appliances", "Temp"] + list(ohe_names)

    importances = pd.Series(
        model.named_steps["regressor"].feature_importances_,
        index=all_names
    ).sort_values()

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    importances.tail(10).plot(kind="barh", color="#3498db", ax=ax2)
    ax2.set_title("Top 10 Drivers")
    st.pyplot(fig2)


with st.expander("🔍 Raw input sent to model"):
    st.dataframe(input_row, use_container_width=True)

