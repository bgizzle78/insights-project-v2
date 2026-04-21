# ---- Imports ----
import pandas as pd

# =====================================
# FUNCTIONS
# =====================================
# =====================================
# CORE GROWTH ENGINE (NEW - CRITICAL)
# =====================================
def calculate_growth(df, value_col, group_col='industry', year_col='year'):
    df = df.sort_values([group_col, year_col]).copy()

    df['prev_value'] = df.groupby(group_col)[value_col].shift(1)

    df[f'{value_col}_growth'] = (
        (df[value_col] - df['prev_value']) / df['prev_value']
    )

    df = df.drop(columns=['prev_value'])

    return df

# =====================================
# WRAPPERS (STANDARDIZED)
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
# SHARE METRICS (SAFE VERSION)
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
# PERFORMANCE SUMMARY (NEW - REPLACES PAGE LOGIC)
# =====================================
def build_performance_summary(df, group_col='industry', year_col='year'):
    df = df.sort_values([group_col, year_col])

    years = df[year_col].nunique()

    base = df.groupby(group_col).agg(
        employment=('employment', 'sum'),
        gdp=('gdp', 'sum')
    ).reset_index()

    # MULTI-YEAR → TRUE GROWTH
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

        growth['size_metric'] = growth['end_emp']

        result = growth

    # SINGLE YEAR → TRUE SNAPSHOT (NO AGGREGATION)
    else:
        result = df.copy()

        # One row per industry already → no need to sum
        result = result[[group_col, 'employment', 'gdp']]

        # Normalize safely
        result['emp_metric'] = result['employment'] / result['employment'].max()
        result['gdp_metric'] = result['gdp'] / result['gdp'].max()

        result['size_metric'] = result['employment']

        # CLEAN
        result = result.replace([float('inf'), -float('inf')], None).dropna()
        result = result.drop_duplicates(subset=[group_col])

    return result