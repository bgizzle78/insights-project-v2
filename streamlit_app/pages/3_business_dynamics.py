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
import plotly.graph_objects as go
from utils.ui import render_kpi_card
from utils.data_loader import load_economic_data

# =====================================
# PAGE TITLE
# =====================================
st.title('🏢 Business Dynamics & Formation Trends')

# =====================================
# LOAD DATA
# =====================================
df = load_economic_data()
df['year'] = df['year'].astype(int)

# =====================================
# FILTER BAR (GLOBAL STYLE)
# =====================================
st.subheader('🔎 Filters')

industries = sorted(df['industry'].dropna().unique())

col1, col2 = st.columns([2, 1])

with col1:
    select_all = st.checkbox('Select All Industries', value=True)

    selected_industry = st.selectbox(
        'Select Industry',
        options=industries,
        disabled=select_all
    )

    if select_all:
        selected_industries = industries
    else:
        selected_industries = [selected_industry]

st.divider()

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
# KPI CARDS (GLOBAL STYLE)
# =====================================
st.subheader('📊 Business Metrics')

latest = df_business.sort_values('year').iloc[-1]

total_filings = latest['new_filings']
total_terminations = latest['terminations']
net_total = latest['net_change']

cols = st.columns(3)

# ---- New Filings ----
with cols[0]:
    render_kpi_card(
        'New Filings',
        f'{int(total_filings):,}'
    )

# ---- Terminations ----
with cols[1]:
    render_kpi_card(
        'Terminations',
        f'{int(total_terminations):,}'
    )

# ---- Net Growth ----
with cols[2]:
    render_kpi_card(
        'Net Growth',
        f'{int(net_total):,}',
        '#4CAF50' if net_total >= 0 else '#FF6B6B'
    )

# =====================================
# CHARTS
# =====================================

# Filings vs Terminations
st.subheader('📈 Business Activity Over Time')

fig_activity = go.Figure()

fig_activity.add_trace(go.Scatter(
    x=df_business['year'],
    y=df_business['new_filings'],
    mode='lines+markers',
    line=dict(shape='spline'),
    name='New Filings',
    hovertemplate='Year: %{x}<br>New Filings: %{y:,.0f}<extra></extra>'
))

fig_activity.add_trace(go.Scatter(
    x=df_business['year'],
    y=df_business['terminations'],
    mode='lines+markers',
    line=dict(shape='spline'),
    name='Terminations',
    hovertemplate='Year: %{x}<br>Terminations: %{y:,.0f}<extra></extra>'
))

fig_activity.update_layout(
    xaxis_title='Year',
    yaxis_title='Count',
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_activity, use_container_width=True)

# Net business growth
st.subheader('📊 Net Business Growth')

fig_net = go.Figure()

fig_net.add_trace(go.Scatter(
    x=df_business['year'],
    y=df_business['net_change'],
    mode='lines+markers',
    line=dict(shape='spline'),
    hovertemplate='Year: %{x}<br>Net Growth: %{y:,.0f}<extra></extra>'
))

fig_net.update_layout(
    xaxis_title='Year',
    yaxis_title='Net Change',
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_net, use_container_width=True)

# =====================================
# DATA TABLE
# =====================================
st.subheader('📊 Data View')

df_display = df_business.copy()

# ---- CLEAN COLUMN NAMES ----
df_display.columns = (
    df_display.columns
    .str.replace('_', ' ')
    .str.title()
)

# ---- FORMAT NUMERIC COLUMNS ----
if 'New Filings' in df_display.columns:
    df_display['New Filings'] = df_display['New Filings'].apply(lambda x: f'{x:,.0f}')

if 'Terminations' in df_display.columns:
    df_display['Terminations'] = df_display['Terminations'].apply(lambda x: f'{x:,.0f}')

if 'Net Change' in df_display.columns:
    df_display['Net Change'] = df_display['Net Change'].apply(lambda x: f'{x:,.0f}')

# ---- RENDER TABLE ----
st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)