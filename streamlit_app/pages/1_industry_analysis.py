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
from utils.data_loader import load_economic_data
from utils.metrics import (
    add_growth_metrics,
    add_business_metrics,
    add_share_metrics,
    build_performance_summary,
    get_analysis_snapshot,
    build_ranked_bar_chart
)

# =====================================
# PAGE TITLE
# =====================================
st.title('📊 Industry Analysis')

# =====================================
# LOAD DATA
# =====================================
df = load_economic_data()

# =====================================
# FILTER BAR
# =====================================
st.subheader('🔎 Filters')

view_mode = st.radio(
    'View Mode',
    ['Growth (Multi-Year)', 'Snapshot (Single Year)'],
    horizontal=True
)

industries = sorted(df['industry'].dropna().unique())

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    select_all = st.checkbox('Select All Industries', value=True)

    if select_all:
        selected_industries = industries
    else:
        selected_industries = st.selectbox(
            'Select Industry',
            options=industries
        )
        selected_industries = [selected_industries]

with col2:
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    selected_years = st.slider(
        'Year Range',
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

# =====================================
# ENFORCE VIEW MODE RULES
# =====================================
if view_mode == 'Snapshot (Single Year)':
    # force single year
    selected_years = (selected_years[1], selected_years[1])

if view_mode == 'Growth (Multi-Year)' and selected_years[0] == selected_years[1]:
    st.warning('Select a range of at least 2 years for Growth mode')
    st.stop()

with col3:
    if st.button('Reset Filters'):
        selected_industries = industries
        selected_years = (min_year, max_year)

st.divider()

# =====================================
# APPLY FILTERS
# =====================================
df_filtered = df[
    (df['industry'].isin(selected_industries)) &
    (df['year'].between(selected_years[0], selected_years[1]))
]

# ✅ APPLY METRICS HERE (AFTER FILTERING)
df_filtered = add_growth_metrics(df_filtered)
df_filtered = add_business_metrics(df_filtered)
df_filtered = add_share_metrics(df_filtered)

# =====================================
# KPI CARDS
# =====================================
st.subheader('📈 Key Metrics')

df_kpi = get_analysis_snapshot(df_filtered)

total_employment = df_kpi['employment'].sum()
total_gdp = df_kpi['gdp'].sum()

gdp_per_worker = (total_gdp * 1_000_000) / total_employment if total_employment else 0

col1, col2, col3 = st.columns(3)

# ----- EMPLOYMENT CARD -----
col1.metric(
    'Total Employment',
    f'{int(total_employment):,}'
)

# ----- GDP CARD -----
gdp_display = (
    f'${total_gdp/1_000:,.2f}B'
    if total_gdp < 1_000_000
    else f'${total_gdp/1_000_000:,.2f}T'
)

col2.metric(
    'Total GDP',
    gdp_display
)

# ----- GDP PER WORKER CARD -----
col3.metric(
    'GDP per Worker',
    f'${gdp_per_worker:,.0f}'
)

st.divider()

# =====================================
# DATA TABLE
# =====================================
st.subheader('📊 Industry Data Explorer')
st.caption('Explore raw data or high-level insights')

tab1, tab2 = st.tabs(['📋 Raw Data', '📈 Summary Insights'])

# ---------- TAB 1 — RAW DATA ----------
with tab1:

    df_display = df_filtered.copy()

    # ---- FIX GDP PER WORKER SCALING ----
    if 'gdp_per_worker' in df_display.columns:
        df_display['gdp_per_worker'] = df_display['gdp_per_worker'] * 1_000_000

    # ---- CLEAN COLUMN NAMES ----
    df_display.columns = (
        df_display.columns
        .str.replace('_', ' ')
        .str.title()
    )

    # ---- FORMAT EMPLOYMENT FOR DISPLAY ONLY ----
    if 'Employment' in df_display.columns:
        df_display['Employment'] = df_display['Employment'].apply(
            lambda x: f"{x:,.0f}"
        )

    # ---- FORMAT GDP (MILLIONS DISPLAY) ----
    if 'Gdp' in df_display.columns:
        df_display['Gdp'] = df_display['Gdp'].apply(
            lambda x: f'${x/1000:,.2f}M' if x >= 1000 else f'${x:,.0f}K'
        )

    # ---- FORMAT GDP PER WORKER FOR DISPLAY ONLY ----
    if 'Gdp Per Worker' in df_display.columns:
        df_display['Gdp Per Worker'] = df_display['Gdp Per Worker'].apply(
            lambda x: f'${x:,.0f}'
        )

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

# ---------- TAB 2 — SUMMARY INSIGHTS ----------
with tab2:

    summary = get_analysis_snapshot(df_filtered)

    # AGGREGATE BUSINESS FLOW ONLY
    summary = summary.groupby('industry').agg({
        'employment': 'sum',
        'gdp': 'sum',
        'new_filings': 'sum',
        'terminations': 'sum'
    }).reset_index()

    summary['net_business'] = summary['new_filings'] - summary['terminations']

    summary['employment_share'] = summary['employment'] / summary['employment'].sum()

    summary['gdp_per_worker'] = (
        (summary['gdp'] * 1_000_000) / summary['employment']
)

    summary['importance_score'] = (
        summary['employment_share'] * 0.5 +
        (summary['gdp_per_worker'] / summary['gdp_per_worker'].max()) * 0.5
     )
    
    summary = summary[[
        'industry',
        'employment',
        'employment_share',
        'gdp',
        'gdp_per_worker',
        'new_filings',
        'terminations',
        'net_business',
        'importance_score'
    ]]

    summary = summary.sort_values('importance_score', ascending=False)

    # ---- CLEAN DISPLAY COPY ----
    summary_display = summary.copy()

    summary_display.columns = (
        summary_display.columns
        .str.replace('_', ' ')
        .str.title()
    )

    # ---- KPI SUMMARY ----
    top = summary.sort_values('importance_score', ascending=False).iloc[0]

    st.markdown('### 🏆 Top Performing Industry')

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
    'Industry',
    top['industry'],
    help=top['industry']
    )

    col2.metric(
        'GDP',
        f'${top['gdp']/1_000:,.2f}B'
    )

    col3.metric(
        'Employment',
        f'{top['employment']:,.0f}'
    )

    net = int(top['net_business'])

    col4.metric(
        'Net Growth',
        f'{net:,.0f}',
        delta=net
    )

    st.divider()

    # ---- DEFINE FORMAT RULES ----
    format_dict = {
    'Gdp': lambda x: f'${x/1000:,.2f}B',
    'Gdp Per Worker': '${:,.0f}',
    'Employment': '{:,.0f}',
    'New Filings': '{:,.0f}',
    'Terminations': '{:,.0f}',
    'Net Business': '{:,.0f}',
    'Employment Share': '{:,.1%}',
    'Importance Score': '{:,.2f}'
}
    # ---- TABLE DISPLAY ----
    styled_summary = summary_display.copy()

    styled_summary = styled_summary.style.format(format_dict)

    styled_summary = styled_summary.background_gradient(
        subset=['Gdp', 'Net Business'],
        cmap='RdYlGn'
    )

    # ---- APPLY COLOR GRADIENTS ----
    if 'Gdp' in summary_display.columns:
        styled_summary = styled_summary.background_gradient(
            subset=['Gdp'],
            cmap='Greens'
        )

    if 'Net Business' in summary_display.columns:
        styled_summary = styled_summary.background_gradient(
            subset=['Net Business'],
            cmap='RdYlGn'
        )

    # ---- RENDER TABLE ----
    st.dataframe(
        styled_summary,
        use_container_width=True,
        hide_index=True
    )

# =====================================
# INDUSTRY PERFORMANCE DATA PREP (STABLE)
# =====================================
growth_summary = build_performance_summary(df_filtered)

# =====================================
# EMPLOYMENT GROWTH BY INDUSTRY
# =====================================
st.subheader(
    '📈 Employment Growth by Industry'
    if view_mode == 'Growth (Multi-Year)'
    else '📊 Employment by Industry (Selected Year)'
)

if view_mode == 'Growth (Multi-Year)':
    top_emp = growth_summary.sort_values('emp_metric', ascending=False).head(10)
    top_emp['value'] = top_emp['emp_metric'] * 100
    x_label_emp = 'Employment Growth (%)'
else:
    snapshot_df = df_filtered.groupby('industry')['employment'].sum().reset_index()
    snapshot_df['value'] = snapshot_df['employment'] / snapshot_df['employment'].sum() * 100
    x_label_emp = 'Employment Share (%)'

fig_emp_growth = build_ranked_bar_chart(
    df=top_emp if view_mode == 'Growth (Multi-Year)' else snapshot_df,
    value_col='value',
    label_col='industry',
    title=x_label_emp
)

st.plotly_chart(fig_emp_growth, use_container_width=True)

# =====================================
# GDP GROWTH BY INDUSTRY
# =====================================
st.subheader(
    '💰 GDP Growth by Industry' if view_mode == 'Growth (Multi-Year)'
    else '💰 GDP by Industry (Selected Year)'
)

if view_mode == 'Growth (Multi-Year)':
    top_gdp = growth_summary.sort_values('gdp_metric', ascending=False).head(10)
    top_gdp['value'] = top_gdp['gdp_metric'] * 100
else:
    snapshot_df = df_filtered.groupby('industry')['gdp'].sum().reset_index()
    snapshot_df['value'] = snapshot_df['gdp'] / snapshot_df['gdp'].sum() * 100

fig_gdp_growth = build_ranked_bar_chart(
    df=top_gdp if view_mode == 'Growth (Multi-Year)' else snapshot_df,
    value_col='value',
    label_col='industry',
    title='GDP Comparison'
)

st.plotly_chart(fig_gdp_growth, use_container_width=True)

# =====================================
# INDUSTRY PERFORMANCE SCATTER
# =====================================
st.subheader('🎯 Industry Performance: Winners vs Losers')

fig_scatter = go.Figure()

# =====================================
# GROWTH MODE
# =====================================
if view_mode == 'Growth (Multi-Year)':

    x = growth_summary['emp_metric'] * 100
    y = growth_summary['gdp_metric'] * 100
    color = growth_summary['gdp_metric'] * 100
    size = growth_summary['size_metric']

    hover_df = growth_summary

# =====================================
# SNAPSHOT MODE
# =====================================
else:

    snapshot_df = get_analysis_snapshot(df_filtered).groupby('industry').agg({
        'employment': 'sum',
        'gdp': 'sum'
    }).reset_index()

    snapshot_df['emp_share'] = snapshot_df['employment'] / snapshot_df['employment'].sum()
    snapshot_df['gdp_share'] = snapshot_df['gdp'] / snapshot_df['gdp'].sum()

    x = snapshot_df['emp_share'] * 100
    y = snapshot_df['gdp_share'] * 100
    color = snapshot_df['gdp_share'] * 100
    size = snapshot_df['employment']

    hover_df = snapshot_df

# =====================================
# SCATTER PLOT (COMMON)
# =====================================
fig_scatter.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='markers',
    marker=dict(
        size=(size / size.max()) * 25 + 10,
        color=color,
        colorscale='RdYlGn',
        showscale=True,
        opacity=0.75,
        colorbar=dict(title='GDP')
    ),
    text=hover_df['industry'],
    hovertemplate='<b>%{text}</b><br>GDP: %{x:.1f}%<br>Employment: %{y:.1f}%<extra></extra>'
))

fig_scatter.add_hline(y=0, line_dash='dash')
fig_scatter.add_vline(x=0, line_dash='dash')

fig_scatter.update_layout(
    xaxis_title='Employment Metric',
    yaxis_title='GDP Metric',
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig_scatter, use_container_width=True)