# Imports
import pandas as pd

# =====================================
# FUNCTIONS
# =====================================
def add_growth_metrics(df):
    """Adds year-over-year growth for employment and GDP"""
    df = df.sort_values(['industry', 'year'])

    df['emp_growth'] = df.groupby('industry')['employment'].pct_change()
    df['gdp_growth'] = df.groupby('industry')['gdp'].pct_change()

    return df


def add_business_metrics(df):
    """Adds net business growth (new - closed)"""
    df['net_business_growth'] = df['new_filings'] - df['terminations']
    return df


def add_share_metrics(df):
    """Adds each industry's share of total employment per year"""
    total_employment = df.groupby('year')['employment'].transform('sum')
    df['employment_share'] = df['employment'] / total_employment

    return df