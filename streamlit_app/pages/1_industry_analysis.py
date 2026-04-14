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
from data_loader import load_economic_data
import plotly.graph_objects as go

# =====================================
# PAGE TITLE
# =====================================
st.title('📊 Industry Analysis')

# =====================================
# LOAD DATA
# =====================================
df = load_economic_data()

# =====================================
# FILTER BAR (IMPROVED UX)
# =====================================
st.subheader("🔎 Filters")

industries = sorted(df['industry'].dropna().unique())

col1, col2 = st.columns([2, 1])

with col1:
    select_all = st.checkbox("Select All Industries", value=True)

    if select_all:
        selected_industries = st.multiselect(
            "Industries",
            options=industries,
            default=industries
        )
    else:
        selected_industries = st.multiselect(
            "Industries",
            options=industries,
            default=[]
        )

with col2:
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())

    selected_years = st.slider(
        "Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

st.divider()

# =====================================
# APPLY FILTERS
# =====================================
df_filtered = df[
    (df['industry'].isin(selected_industries)) &
    (df['year'].between(selected_years[0], selected_years[1]))
]

# =====================================
# KPIs
# =====================================
st.subheader('📈 Key Metrics')

total_employment = df_filtered['employment'].sum()
total_gdp = df_filtered['gdp'].sum()
gdp_per_worker = total_gdp / total_employment if total_employment else 0

col1, col2, col3 = st.columns(3)

col1.metric('Total Employment', f'{total_employment:,.0f}')
col2.metric('Total GDP', f'${total_gdp:,.0f}')
col3.metric('GDP per Worker', f'${gdp_per_worker:,.2f}')

# =====================================
# DATA TABLE
# =====================================
st.subheader('Filtered Data')
st.dataframe(df_filtered)

# =====================================
# CHART DATA PREP
# =====================================
# Aggregate by year (important for clean lines)
df_trend = (
    df_filtered
    .groupby('year', as_index=False)
    .agg({
        'employment': 'sum',
        'gdp': 'sum'
    })
    .sort_values('year')
)

df_trend['gdp_millions'] = df_trend['gdp'] / 1_000_000

# =====================================
# EMPLOYMENT TREND
# =====================================
st.subheader("📈 Employment Trend")

fig_emp = go.Figure()

fig_emp.add_trace(go.Scatter(
    x=df_trend['year'],
    y=df_trend['employment'],
    mode='lines+markers',
    name='Employment'
))

fig_emp.update_layout(
    xaxis_title="Year",
    yaxis_title="Employment",
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig_emp, use_container_width=True)

# =====================================
# GDP TREND
# =====================================
st.subheader("💰 GDP Trend")

fig_gdp = go.Figure()

fig_gdp.add_trace(go.Scatter(
    x=df_trend['year'],
    y=df_trend['gdp'],
    mode='lines+markers',
    name='GDP'
))

fig_gdp.update_layout(
    xaxis_title="Year",
    yaxis_title="GDP",
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig_gdp, use_container_width=True)

# =====================================
# GDP vs Employment (Dual Axis)
# =====================================
st.subheader('📊 GDP vs Employment')
fig = go.Figure()

# Employment (left axis)
fig.add_trace(
    go.Scatter(
        x=df_trend['year'],
        y=df_trend['employment'],
        name='Employment',
        yaxis='y1',
        mode='lines+markers',
        hovertemplate="Year: %{x}<br>Employment: %{y:,.0f}<extra></extra>"
    )
)

# GDP (right axis)
fig.add_trace(
    go.Scatter(
        x=df_trend['year'],
        y=df_trend['gdp_millions'],
        name='GDP (Millions)',
        yaxis='y2',
        mode='lines+markers',
        hovertemplate="Year: %{x}<br>GDP: $%{y:,.2f}M<extra></extra>"
    )
)

# Layout
fig.update_layout(
    xaxis=dict(title='Year'),

    yaxis=dict(
        title='Employment',
        tickformat=","
    ),

    yaxis2=dict(
        title='GDP (Millions)',
        overlaying='y',
        side='right',
        tickprefix="$",
        ticksuffix="M"
    ),

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),

    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)