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
from data_loader import load_economic_data, load_unemployment_data

# =====================================
# PAGE CONFIG
# =====================================
st.title('📈 Economic Trends')

# =====================================
# LOAD DATA
# =====================================
df = load_economic_data()
df_unemp = load_unemployment_data()

# =====================================
# AGGREGATE DATA (STATEWIDE)
# =====================================
df_trend = (
    df
    .groupby('year', as_index=False)
    .agg({
        'employment': 'sum',
        'gdp': 'sum',
        'new_filings': 'sum',
        'terminations': 'sum'
    })
)

# =====================================
# KPIs
# =====================================
st.subheader('📊 Statewide Overview')

total_employment = df_trend['employment'].sum()
total_gdp = df_trend['gdp'].sum()
total_filings = df_trend['new_filings'].sum()
total_terminations = df_trend['terminations'].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric('Employment', f'{total_employment:,.0f}')
col2.metric('GDP', f'${total_gdp:,.0f}')
col3.metric('New Filings', f'{total_filings:,.0f}')
col4.metric('Terminations', f'{total_terminations:,.0f}')

# =====================================
# CHARTS
# =====================================

# Employment
st.subheader('Employment Over Time')
st.line_chart(df_trend.set_index('year')['employment'])

# GDP
st.subheader('GDP Over Time')
st.line_chart(df_trend.set_index('year')['gdp'])

# Business Activity
st.subheader('Business Activity')

st.line_chart(
    df_trend.set_index('year')[['new_filings', 'terminations']]
)

# =====================================
# UNEMPLOYMENT (MACRO VIEW)
# =====================================
st.subheader('📉 Unemployment Rate')

latest_unemp = df_unemp.sort_values(by='year').iloc[-1]['unemployment_rate']

st.metric('Latest Unemployment Rate', f'{latest_unemp:.2f}%')

st.line_chart(
    df_unemp.set_index('year')['unemployment_rate']
)