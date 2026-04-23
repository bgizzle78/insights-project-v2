# ---- Imports ----
import pandas as pd
import plotly.graph_objects as go

"""Metrics module for feature engineering and analytical transformations.
Used across Streamlit pages to standardize:
- Growth calculations
- Business dynamics
- Employment share metrics"""

# =====================================
# FUNCTIONS
# =====================================

# =====================================
# CORE GROWTH ENGINE
# =====================================
def calculate_growth(df, value_col, group_col='industry', year_col='year'):
    df = df.sort_values([group_col, year_col]).copy()
    df['prev_value'] = df.groupby(group_col)[value_col].shift(1)

    df[f'{value_col}_growth'] = (
        (df[value_col] - df['prev_value']) / df['prev_value']
    )

    # ---- FIX: handle divide-by-zero / invalid cases ----
    df[f'{value_col}_growth'] = df[f'{value_col}_growth'].replace([float('inf'), -float('inf')], None)

    df = df.drop(columns=['prev_value'])
    return df

# =====================================
# FEATURE PIPELINES (APPLY MULTIPLE METRICS)
# =====================================
def add_growth_metrics(df):
    df = calculate_growth(df, 'employment')
    df = calculate_growth(df, 'gdp')
    return df

# =====================================
# BUSINESS METRICS (CLEANED)
# =====================================
def add_business_metrics(df):
    df = df.copy()

    df['net_business_growth'] = df['new_filings'] - df['terminations']

    # Optional but VERY useful for stability later
    df = df.sort_values(['industry', 'year'])
    df['prev_total_business'] = df.groupby('industry')['new_filings'].shift(1)

    df['net_business_rate'] = (
        df['net_business_growth'] / df['prev_total_business']
    )

    df = df.drop(columns=['prev_total_business'])

    return df

# =====================================
# SHARE METRICS
# =====================================
def add_share_metrics(df):
    df = df.copy()

    df['total_employment_year'] = df.groupby('year')['employment'].transform('sum')

    df['employment_share'] = (
        df['employment'] / df['total_employment_year']
    )

    df = df.drop(columns=['total_employment_year'])

    return df

# =====================================
# INDUSTRY PERFORMANCE SUMMARY (FOR VISUALIZATION LAYER)
# =====================================
def build_performance_summary(df, group_col='industry', year_col='year'):
    """Builds an industry-level performance dataset for visualization. Handles both multi-year and single-year datasets by switching between true growth calculation and normalized snapshot metrics."""

    df = df.sort_values([group_col, year_col]).copy()
    years = df[year_col].nunique()

    # =========================================================
    # MULTI-YEAR CASE → TRUE TIME-BASED GROWTH
    # =========================================================
    if years > 1:
        growth = df.groupby(group_col).agg(
            start_emp=('employment', 'first'),
            end_emp=('employment', 'last'),
            start_gdp=('gdp', 'first'),
            end_gdp=('gdp', 'last')
        ).reset_index()

        growth['emp_metric'] = (
            (growth['end_emp'] - growth['start_emp']) /
            growth['start_emp']
        )

        growth['gdp_metric'] = (
            (growth['end_gdp'] - growth['start_gdp']) /
            growth['start_gdp']
        )

        # SIZE proxy for scatter/bubble charts
        growth['size_metric'] = growth['end_emp']

        result = growth

    # =========================================================
    # SINGLE-YEAR CASE → SNAPSHOT NORMALIZATION
    # =========================================================
    else:
        result = df[[group_col, 'employment', 'gdp']].drop_duplicates()

        # Normalize within-year for comparability
        max_emp = result['employment'].max()
        max_gdp = result['gdp'].max()

        result['emp_metric'] = result['employment'] / max_emp if max_emp != 0 else 0
        result['gdp_metric'] = result['gdp'] / max_gdp if max_gdp != 0 else 0

        result['size_metric'] = result['employment']

    # =========================================================
    # CLEANUP STEP (SAFETY LAYER)
    # =========================================================
    result = result.replace([float('inf'), -float('inf')], None).dropna()

    return result

def get_analysis_snapshot(df, year_col='year'):
    """ Returns a dataset standardized to the correct time context.
    - Single-year data → returns unchanged
    - Multi-year data → filters to latest year only
    This ensures consistent KPI and visualization behavior."""

    years = df[year_col].nunique()

    if years == 1:
        return df.copy()

    latest_year = df[year_col].max()
    return df[df[year_col] == latest_year].copy()


def build_ranked_bar_chart(
    df,
    value_col,
    label_col='industry',
    top_n=10,
    title='',
    x_label='',
    value_format='number'  # 'percent' or 'number'
):
    """Builds a clean, self-explanatory horizontal bar chart.
    Parameters:
    - value_format:
        'percent' → formats values as %
        'number' → formats as raw numeric values"""

    df_ranked = df.sort_values(value_col, ascending=False).head(top_n)

    # =====================================
    # FORMAT CONTROL
    # =====================================
    if value_format == 'percent':
        hover_template = '%{y}<br>Value: %{x:.2f}%<extra></extra>'
    else:
        hover_template = '%{y}<br>Value: %{x:,.0f}<extra></extra>'

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_ranked[value_col],
        y=df_ranked[label_col],
        orientation='h',
        hovertemplate=hover_template
    ))

    fig.update_layout(
        title=title,
        xaxis_title=x_label if x_label else value_col.replace('_', ' ').title(),
        yaxis_title=label_col.title(),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig