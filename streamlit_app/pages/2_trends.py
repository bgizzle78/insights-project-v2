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
# PAGE TITLE
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
# KPI CARDS (GLOBAL STYLE)
# =====================================
st.subheader('📊 Statewide Overview')

latest = df_trend.sort_values('year').iloc[-1]
latest_unemp = df_unemp.sort_values('year').iloc[-1]['unemployment_rate']

total_employment = latest['employment']
total_gdp = latest['gdp']
net_business_growth = latest['new_filings'] - latest['terminations']

cols = st.columns(4)

# ---- Employment ----
with cols[0]:
    st.markdown(f'''
    <div style="background-color:#1f1f1f;padding:18px;border-radius:14px;height:130px;line-height: 1.1;">
        <div style="font-size:22px;opacity:0.7;">Employment</div>
        <div style="font-size:28px;font-weight:700;margin-top:10px;">
            {int(total_employment):,}
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ---- GDP ----
with cols[1]:
    st.markdown(f'''
    <div style="background-color:#1f1f1f;padding:18px;border-radius:14px;height:130px;line-height: 1.1;">
        <div style="font-size:22px;opacity:0.7;">GDP</div>
        <div style="font-size:28px;font-weight:700;margin-top:10px;color:#4CAF50;">
            ${int(total_gdp):,}
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ---- Net Business Growth ----
with cols[2]:
    color = '#4CAF50' if net_business_growth >= 0 else '#FF6B6B'

    st.markdown(f'''
    <div style="background-color:#1f1f1f;padding:18px;border-radius:14px;height:130px;line-height: 1.1;">
        <div style="font-size:22px;opacity:0.7;">Net Growth</div>
        <div style="font-size:28px;font-weight:700;margin-top:10px;color:{color};">
            {int(net_business_growth):,}
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ---- Unemployment ----
with cols[3]:
    st.markdown(f'''
    <div style="background-color:#1f1f1f;padding:18px;border-radius:14px;height:130px;line-height: 1.1;">
        <div style="font-size:20px;opacity:0.7;">Unemployment Rate</div>
        <div style="font-size:28px;font-weight:700;margin-top:10px;color:#FF6B6B;">
            {latest_unemp:.2f}%
        </div>
    </div>
    ''', unsafe_allow_html=True)

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