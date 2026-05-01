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
from utils.data_loader import load_economic_data, load_unemployment_data

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
# FORMAT YEAR
# =====================================
df['year'] = df['year'].astype(int)
df_unemp['year'] = df_unemp['year'].astype(int)

# =====================================
# AGGREGATE DATA (STATEWIDE)
# =====================================
df_trend = (
    df
    .groupby('year', as_index=False)
    .agg({
        'employment': 'sum'
    })
)

# =====================================
# KPI CARDS (GLOBAL STYLE)
# =====================================
st.subheader('📊 Statewide Overview for 2024')

latest = df_trend.sort_values('year').iloc[-1]
latest_unemp = df_unemp.sort_values('year').iloc[-1]['unemployment_rate']

total_employment = latest['employment']
latest_labor_force = df_unemp.sort_values('year').iloc[-1]['labor_force']
latest_lfpr = df_unemp.sort_values('year').iloc[-1]['labor_force_participation_rate']

cols = st.columns(4)

# ---- Employment ----
with cols[0]:
    render_kpi_card(
        'Employment',
        f'{int(total_employment):,}'
    )

# ---- Unemployment ----
with cols[1]:
    render_kpi_card(
        'Unemployment Rate',
        f'{latest_unemp:.2f}%',
        '#FF6B6B'
    )

# ---- Labor Force ----
with cols[2]:
    render_kpi_card(
        'Labor Force',
        f'{int(latest_labor_force):,}'
    )

# ---- LFPR ----
with cols[3]:
    render_kpi_card(
        'LFPR',
        f'{latest_lfpr:.2f}%',
        '#4CAF50'
    )

# =====================================
# CHARTS
# =====================================

 # ---- EMPLOYMENT ----
st.subheader('👷 Employment')

fig_emp = go.Figure()

fig_emp.add_trace(go.Scatter(
    x=df_trend['year'],
    y=df_trend['employment'],
    mode='lines+markers',
    line=dict(shape='spline'),
    hovertemplate='Year: %{x}<br>Employment: %{y:,.0f}<extra></extra>'
))

fig_emp.update_layout(
    xaxis_title='Year',
    yaxis_title='Employment',
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_emp, use_container_width=True)

# ---- UNEMPLOYMENT ----
st.subheader('📉 Unemployment Rate')

fig_unemp = go.Figure()

fig_unemp.add_trace(go.Scatter(
    x=df_unemp['year'],
    y=df_unemp['unemployment_rate'],
    mode='lines+markers',
    line=dict(shape='spline'),
    hovertemplate='Year: %{x}<br>Unemployment: %{y:.2f}%<extra></extra>'
))

fig_unemp.update_layout(
    xaxis_title='Year',
    yaxis_title='Unemployment Rate (%)',
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_unemp, use_container_width=True)

# ---- LABOR FORCE ----
st.subheader('🧑‍💼 Labor Force')

fig_lf = go.Figure()

fig_lf.add_trace(go.Scatter(
    x=df_unemp['year'],
    y=df_unemp['labor_force'],
    mode='lines+markers',
    line=dict(shape='spline'),
    hovertemplate='Year: %{x}<br>Labor Force: %{y:,.0f}<extra></extra>'
))

fig_lf.update_layout(
    xaxis_title='Year',
    yaxis_title='Labor Force',
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_lf, use_container_width=True)

# ---- LABOR FORCE PARTICIPATION RATE ----
st.subheader('📊 Labor Force Participation Rate')

fig_lfpr = go.Figure()

fig_lfpr.add_trace(go.Scatter(
    x=df_unemp['year'],
    y=df_unemp['labor_force_participation_rate'],
    mode='lines+markers',
    line=dict(shape='spline'),
    hovertemplate='Year: %{x}<br>LFPR: %{y:.2f}%<extra></extra>'
))

fig_lfpr.update_layout(
    xaxis_title='Year',
    yaxis_title='LFPR (%)',
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_lfpr, use_container_width=True)