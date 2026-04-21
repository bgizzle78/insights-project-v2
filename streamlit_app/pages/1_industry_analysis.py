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
from utils.metrics import (
    add_growth_metrics,
    add_business_metrics,
    add_share_metrics,
    build_performance_summary
)
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
st.subheader('🔎 Filters')

industries = sorted(df['industry'].dropna().unique())

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    select_all = st.checkbox('Select All Industries', value=True)

    if select_all:
        selected_industries = st.multiselect(
            'Industries',
            options=industries,
            default=industries,
            placeholder='Select industries...'
        )
    else:
        selected_industries = st.multiselect(
            'Industries',
            options=industries,
            default=[]
        )

with col2:
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())

    selected_years = st.slider(
        'Year Range',
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

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
# VIEW MODE DETECTION
# =====================================

is_single_year = selected_years[0] == selected_years[1]

# =====================================
# KPI CARDS (GLOBAL STYLE)
# =====================================
st.subheader('📈 Key Metrics')

years_selected = df_filtered['year'].nunique()

# SINGLE YEAR → use data directly
if years_selected == 1:
    total_employment = df_filtered['employment'].sum()
    total_gdp = df_filtered['gdp'].sum()

# MULTI YEAR → use latest year snapshot (NOT SUM)
else:
    latest_year = df_filtered['year'].max()
    df_latest = df_filtered[df_filtered['year'] == latest_year]

    total_employment = df_latest['employment'].sum()
    total_gdp = df_latest['gdp'].sum()

gdp_per_worker = (total_gdp * 1_000_000) / total_employment if total_employment else 0

card1, card2, card3 = st.columns(3)

# ---- Employment Card ----
with card1:
    st.markdown(f'''
    <div style="
        background-color: #1f1f1f;
        padding: 18px;
        border-radius: 14px;
        height: 130px;
        line-height: 1.1;
    ">
        <div style="font-size: 24px; opacity: 0.7;">Total Employment</div>
        <div style="font-size: 30px; font-weight: 700; margin-top: 10px;">
            {int(total_employment):,}
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ---- GDP Card ----
with card2:
    gdp_display = f'${total_gdp/1_000:,.2f}B' if total_gdp < 1_000_000 else f'${total_gdp/1_000_000:,.2f}T'

    st.markdown(f'''
    <div style="
        background-color: #1f1f1f;
        padding: 18px;
        border-radius: 14px;
        height: 130px;
        line-height: 1.1;
    ">
        <div style="font-size: 24px; opacity: 0.7;">Total GDP</div>
        <div style="font-size: 30px; font-weight: 700; margin-top: 10px; color: #2ecc71;">
            {gdp_display}
        </div>
    </div>
    ''', unsafe_allow_html=True)

# ---- GDP per Worker Card ----
with card3:

    st.markdown(f'''
    <div style="
        background-color: #1f1f1f;
        padding: 18px;
        border-radius: 14px;
        height: 130px;
        line-height: 1.1;
    ">
        <div style="font-size: 24px; opacity: 0.7;">GDP per Worker</div>
        <div style="font-size: 30px; font-weight: 700; margin-top: 10px;">
            ${gdp_per_worker:,.0f}
        </div>
    </div>
    ''', unsafe_allow_html=True)

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

    # ---- SUMMARY AGGREGATION ----
    years_selected = df_filtered['year'].nunique()

    # SINGLE YEAR → direct snapshot
    if years_selected == 1:
        summary = df_filtered.copy()

    # MULTI YEAR → use latest year snapshot
    else:
        latest_year = df_filtered['year'].max()
        summary = df_filtered[df_filtered['year'] == latest_year].copy()

    # NOW SAFE TO AGGREGATE BUSINESS FLOW ONLY
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

    # ---- KPI CARDS ----
    top = summary.sort_values('importance_score', ascending=False).iloc[0]

    st.markdown('### 🏆 Top Performing Industry')

    card_col1, card_col2, card_col3, card_col4 = st.columns(4)

    with card_col1:
        st.markdown(f'''
        <div style="
            background-color: #1f1f1f;
            padding: 12px;
            border-radius: 12px;
            height: 140px;
            line-height: 1.1;
        ">
            <div style="font-size: 20px; opacity: 0.7;">Industry</div>
            <div style="font-size: 18px; font-weight: 600; line-height: 1.3; white-space: normal; overflow-wrap: break-word;">
                {top['industry']}
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with card_col2:
        st.markdown(f'''
        <div style="
            background-color: #1f1f1f;
            padding: 12px;
            border-radius: 12px;
            height: 140px;
            line-height: 1.1;
        ">
            <div style="font-size: 20px; opacity: 0.7;">GDP</div>
            <div style="font-size: 26px; font-weight: 700; color: #2ecc71;">
                ${top['gdp']/1_000:,.2f}B
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with card_col3:
        st.markdown(f'''
        <div style="
            background-color: #1f1f1f;
            padding: 12px;
            border-radius: 12px;
            height: 140px;
            line-height: 1.1;
        ">
            <div style="font-size: 20px; opacity: 0.7;">Employment</div>
            <div style="font-size: 26px; font-weight: 700;">
                {top['employment']:,.0f}
            </div>
        </div>
        ''', unsafe_allow_html=True)

    net = top['net_business']
    color = '#2ecc71' if net >= 0 else '#e74c3c'

    with card_col4:
        st.markdown(f'''
        <div style="
            background-color: #1f1f1f;
            padding: 12px;
            border-radius: 12px;
            height: 140px;
            line-height: 1.1;
        ">
            <div style="font-size: 20px; opacity: 0.7;">Net Growth</div>
            <div style="font-size: 26px; font-weight: 700; color: {color};">
                {net:,.0f}
            </div>
        </div>
        ''', unsafe_allow_html=True)

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
    styled_summary = summary_display.style.format(format_dict)

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
    '📈 Employment Growth by Industry' if not is_single_year
    else '📊 Employment by Industry (Selected Year)'
)

top_emp = growth_summary.sort_values('emp_metric', ascending=False).head(10)

fig_emp_growth = go.Figure()

fig_emp_growth.add_trace(go.Bar(
    x=top_emp['emp_metric'] * 100,
    y=top_emp['industry'],
    orientation='h',
    hovertemplate='%{y}<br>Growth: %{x:.2f}%<extra></extra>'
))

fig_emp_growth.update_layout(
    xaxis_title='Employment Growth (%)' if not is_single_year else 'Relative Employment',
    yaxis_title='Industry',
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig_emp_growth, use_container_width=True)

# =====================================
# GDP GROWTH BY INDUSTRY
# =====================================
st.subheader(
    '💰 GDP Growth by Industry' if not is_single_year
    else '💰 GDP by Industry (Selected Year)'
)

top_gdp = growth_summary.sort_values('gdp_metric', ascending=False).head(10)

fig_gdp_growth = go.Figure()

fig_gdp_growth.add_trace(go.Bar(
    x=top_gdp['gdp_metric'] * 100,
    y=top_gdp['industry'],
    orientation='h',
    hovertemplate='%{y}<br>Growth: %{x:.2f}%<extra></extra>'
))

fig_gdp_growth.update_layout(
    xaxis_title='GDP Growth (%)' if not is_single_year else 'Relative GDP',
    yaxis_title='Industry',
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig_gdp_growth, use_container_width=True)

# =====================================
# INDUSTRY PERFORMANCE SCATTER
# =====================================

if growth_summary is None or growth_summary.empty:
    st.warning("Not enough data for scatter plot")

else:
    st.subheader('🎯 Industry Performance: Winners vs Losers')

    fig_scatter = go.Figure()

    # =====================================
    # MULTI-YEAR MODE (TRUE GROWTH)
    # =====================================
    if df_filtered['year'].nunique() > 1:

        x = growth_summary['emp_metric'] * 100
        y = growth_summary['gdp_metric'] * 100
        color = growth_summary['gdp_metric'] * 100

        

    # =====================================
    # SINGLE-YEAR MODE (STRUCTURE SNAPSHOT)
    # =====================================
    else:

        x = growth_summary['emp_metric'] * 100
        y = growth_summary['gdp_metric'] * 100
        color = growth_summary['gdp_metric'] * 100

        

    fig_scatter.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',

        marker=dict(
            size=(
                (growth_summary['size_metric'] /
                 growth_summary['size_metric'].max()) * 25
            ) + 10,
            color=color,
            colorscale='RdYlGn',
            showscale=True,
            opacity=0.75,
            colorbar=dict(title='GDP ')
        ),

        text=growth_summary['industry'],

        hovertemplate=(
            '<b>%{text}</b><br>'
            'Employment: %{x:.1f}<br>'
            'GDP: %{y:.1f}<extra></extra>'
        )
    ))

    fig_scatter.add_hline(y=0, line_dash='dash')
    fig_scatter.add_vline(x=0, line_dash='dash')

    fig_scatter.update_layout(
        xaxis_title='Employment ',
        yaxis_title='GDP ',
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig_scatter, use_container_width=True)