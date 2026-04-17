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

# =====================================
# KPI CARDS (GLOBAL STYLE)
# =====================================

st.subheader('📈 Key Metrics')

total_employment = df_filtered['employment'].sum()
total_gdp = df_filtered['gdp'].sum()

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
    summary = df_filtered.groupby('industry').agg({
        'employment': 'sum',
        'gdp': 'sum',
        'new_filings': 'sum',
        'terminations': 'sum'
    }).reset_index()

    summary['net_business'] = summary['new_filings'] - summary['terminations']

    summary['gdp_per_worker'] = (
        (summary['gdp'] * 1_000_000) / summary['employment']
    )

    summary = summary.sort_values('gdp', ascending=False)

    # ---- CLEAN DISPLAY COPY ----
    summary_display = summary.copy()

    summary_display.columns = (
        summary_display.columns
        .str.replace('_', ' ')
        .str.title()
    )

    # ---- KPI CARDS ----
    top = summary.iloc[0]

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
    'Net Business': '{:,.0f}'
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

df_trend['gdp_billions'] = df_trend['gdp'] / 1_000_000_000

# =====================================
# EMPLOYMENT TREND
# =====================================
st.subheader('📈 Employment Trend')

fig_emp = go.Figure()

fig_emp.add_trace(go.Scatter(
    x=df_trend['year'],
    y=df_trend['employment']/1_000,
    mode='lines+markers',
    name='Employment',
    hovertemplate='Year: %{x}<br>Employment: %{y:,.1f}K<extra></extra>'
))

fig_emp.update_layout(
    xaxis_title='Year',
    yaxis_title='Employment',
    yaxis=dict(ticksuffix='K'),
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig_emp, use_container_width=True)

# =====================================
# GDP TREND
# =====================================
st.subheader('💰 GDP Trend')

fig_gdp = go.Figure()

fig_gdp.add_trace(go.Scatter(
    x=df_trend['year'],
    y=df_trend['gdp'] / 1000,
    mode='lines+markers',
    name='GDP',
    hovertemplate='Year: %{x}<br>GDP: $%{y:,.2f}B<extra></extra>'
))

fig_gdp.update_layout(
    xaxis_title='Year',
    yaxis_title='GDP (Billions)',
    yaxis=dict(tickprefix='$', ticksuffix='B'),
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
        y=df_trend['employment']/1_000,
        name='Employment',
        yaxis='y1',
        mode='lines+markers',
        hovertemplate='Year: %{x}<br>Employment: %{y:,.1f}K<extra></extra>'
    )
)

# GDP (right axis)
fig.add_trace(
    go.Scatter(
        x=df_trend['year'],
        y=df_trend['gdp'] / 1000,
        name='GDP (Billions)',
        yaxis='y2',
        mode='lines+markers',
        hovertemplate='Year: %{x}<br>GDP: $%{y:,.2f}B<extra></extra>'
    )
)

# Layout
fig.update_layout(
    xaxis=dict(title='Year'),

    yaxis=dict(
        title='Employment (Thousands)',
        tickformat=',',
        ticksuffix='K'
    ),

    yaxis2=dict(
        title='GDP (Billions)',
        overlaying='y',
        side='right',
        tickprefix='$',
        ticksuffix='B'
    ),

    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),

    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)