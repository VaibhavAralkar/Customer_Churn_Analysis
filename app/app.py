import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# --- PostgreSQL Connection Configuration ---
DB_CONFIG = {
    "host": "db",  # Use "db" if running in Docker Compose
    "port": 5432,
    "user": "postgres",
    "password": "root",
    "database": "prediction_data"
}

TABLE_NAME = "customer_data_cleaned"

# --- Set up connection string ---
engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# --- Page Config ---
st.set_page_config(page_title="Telecom Customer Churn Dashboard", layout="wide")
st.title("📊 Telecom Customer Churn Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_sql_table(TABLE_NAME, con=engine)
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Contract Type (Single Select with 'All')
contract_types = ['All'] + sorted(df['contracttype'].dropna().unique().tolist())
selected_contract_type = st.sidebar.selectbox(
    "Select Contract Type:",
    options=contract_types,
    index=0  # Default to 'All'
)

# Internet Service (Single Select with 'All')
internet_services = ['All'] + sorted(df['internetservice'].dropna().unique().tolist())
selected_internet_service = st.sidebar.selectbox(
    "Select Internet Service:",
    options=internet_services,
    index=0  # Default to 'All'
)

# Churn (Single Select with 'All')
churn_options = ['All', True, False]
selected_churn = st.sidebar.selectbox(
    "Select Churn:",
    options=churn_options,
    index=0  # Default to 'All'
)

# Reset Button
if st.sidebar.button("Reset Filters"):
    st.experimental_rerun()

# --- Data Filtering ---
filtered_df = df.copy()

if selected_contract_type != 'All':
    filtered_df = filtered_df[filtered_df['contracttype'] == selected_contract_type]

if selected_internet_service != 'All':
    filtered_df = filtered_df[filtered_df['internetservice'] == selected_internet_service]

if selected_churn != 'All':
    filtered_df = filtered_df[filtered_df['churn'] == selected_churn]

# --- Top Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{len(filtered_df)}")
col2.metric("Churned Customers", f"{filtered_df['churn'].sum()}")
col3.metric("Churn Rate", f"{filtered_df['churn'].mean() * 100:.2f}%" if len(filtered_df) > 0 else "N/A")

# --- Financials ---
st.subheader("💰 Financial Overview")
col4, col5, col6 = st.columns(3)
col4.metric("Avg Monthly Charges", f"₹{filtered_df['monthlycharges'].mean():.2f}" if len(filtered_df) > 0 else "N/A")
col5.metric("Total Revenue", f"₹{filtered_df['totalcharges'].sum():,.2f}")
col6.metric("Lost Revenue (Churned)", f"₹{filtered_df[filtered_df['churn'] == True]['totalcharges'].sum():,.2f}")

# --- Churn by Contract Type ---
st.subheader("📄 Churn Rate by Contract Type")
churn_by_contract = filtered_df.groupby("contracttype")["churn"].mean().reset_index()
fig1 = px.bar(
    churn_by_contract,
    x="contracttype",
    y="churn",
    title="Churn Rate by Contract Type",
    labels={"churn": "Churn Rate"},
    text_auto=".2%"
)
st.plotly_chart(fig1, use_container_width=True)

# --- Churn by Internet Service ---
st.subheader("🌐 Churn Rate by Internet Service")
churn_by_internet = filtered_df.groupby("internetservice")["churn"].mean().reset_index()
fig2 = px.bar(
    churn_by_internet,
    x="internetservice",
    y="churn",
    title="Churn Rate by Internet Service",
    labels={"churn": "Churn Rate"},
    text_auto=".2%"
)
st.plotly_chart(fig2, use_container_width=True)

# --- Churn by Gender ---
st.subheader("👥 Churn Rate by Gender")
churn_by_gender = filtered_df.groupby("gender")["churn"].mean().reset_index()
fig3 = px.pie(
    churn_by_gender,
    names="gender",
    values="churn",
    title="Churn Rate by Gender",
    hole=0.4
)
st.plotly_chart(fig3, use_container_width=True)

# --- Tenure Distribution ---
st.subheader("⏳ Tenure Distribution")
fig4 = px.histogram(
    filtered_df,
    x="tenure",
    nbins=30,
    title="Customer Tenure Distribution",
    labels={"tenure": "Tenure (Months)"}
)
st.plotly_chart(fig4, use_container_width=True)

# --- Total Charges by Churn (with Outliers) ---
st.subheader("📈 Total Charges Distribution by Churn (with Outliers)")
fig6 = px.box(
       filtered_df,
       x="churn",
       y="totalcharges",
       points="outliers",
       color="churn",
       title="Total Charges by Churn",
       labels={"churn": "Churn", "totalcharges": "Total Charges (₹)"}
    )
st.plotly_chart(fig6, use_container_width=True)

# --- Tech Support Impact ---
st.subheader("🛠️ Churn Rate by Tech Support")
churn_by_support = filtered_df.groupby("techsupport")["churn"].mean().reset_index()
fig7 = px.bar(
    churn_by_support,
    x="techsupport",
    y="churn",
    title="Churn Rate by Tech Support",
    labels={"churn": "Churn Rate"},
    text_auto=".2%"
)
st.plotly_chart(fig7, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("🔍 Data source: Cleaned Telecom Customer Churn dataset from PostgreSQL")
