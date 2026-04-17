# =====================================
# FIX PYTHON PATH
# =====================================
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# =====================================
# IMPORTS
# =====================================
import streamlit as st
from utils.data_loader import load_economic_data

# =====================================
# PAGE TITLE
# =====================================
st.title('🏢 Business Dynamics')

# =====================================
# LOAD DATA
# =====================================
df = load_economic_data()

# =====================================
# SIDEBAR FILTERS
# =====================================
st.sidebar.header('Filters')

industries = sorted(df['industry'].dropna().unique())
selected_industries = st.sidebar.multiselect(
    'Select Industry',
    options=industries,
    default=industries
)

# =====================================
# APPLY FILTER
# =====================================
df_filtered = df[
    df['industry'].isin(selected_industries)
]

# =====================================
# AGGREGATE DATA
# =====================================
df_business = (
    df_filtered
    .groupby('year', as_index=False)
    .agg({
        'new_filings': 'sum',
        'terminations': 'sum'
    })
)

# Net business creation
df_business['net_change'] = (
    df_business['new_filings'] - df_business['terminations']
)

# =====================================
# KPIs
# =====================================
st.subheader('📊 Business Metrics')

total_filings = df_business['new_filings'].sum()
total_terminations = df_business['terminations'].sum()
net_total = df_business['net_change'].sum()

col1, col2, col3 = st.columns(3)

col1.metric('New Filings', f'{total_filings:,.0f}')
col2.metric('Terminations', f'{total_terminations:,.0f}')
col3.metric('Net Change', f'{net_total:,.0f}')

# =====================================
# CHARTS
# =====================================

# Filings vs Terminations
st.subheader('Business Activity Over Time')

st.line_chart(
    df_business.set_index('year')[['new_filings', 'terminations']]
)

# Net Change
st.subheader('Net Business Creation')

st.line_chart(
    df_business.set_index('year')['net_change']
)

# =====================================
# DATA TABLE
# =====================================
st.subheader('Data View')
st.dataframe(df_business)