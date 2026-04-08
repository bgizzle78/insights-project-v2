# Imports
import pandas as pd
from src.config import START_YEAR, END_YEAR
from src.config import CSV_EXPORT_KWARGS


# Column Cleaning
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes column names:
    - lowercase
    - replaces spaces with underscores
    - removes special characters"""

    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r'(?<!^)(?=[A-Z])', '_', regex=True)
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^\w_]', '', regex=True)
    )
    return df


# Date Parsing
def parse_dates(df: pd.DataFrame, date_columns: list) -> pd.DataFrame:
    """Converts columns to datetime safely."""

    df = df.copy()
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


# Fill Unknown Categories
def fill_unknown(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Fills missing categorical values with 'unknown'."""

    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = df[col].fillna('unknown')
    return df


# Filter by Year Range
def filter_year_range(df: pd.DataFrame, date_column: str, start_year: int = START_YEAR, end_year: int = END_YEAR) -> pd.DataFrame:
    df = df.copy()
    df['year'] = df[date_column].dt.year
    df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    return df


# Extract Year Columns
def add_year_columns(df: pd.DataFrame, date_columns: dict) -> pd.DataFrame:
    """Adds year columns from datetime columns.
    Example input: {'filing_date': 'filing_year'}"""

    df = df.copy()
    for date_col, year_col in date_columns.items():
        if date_col in df.columns:
            df[year_col] = df[date_col].dt.year
    return df


# WVSOS Industry Mapping
def map_naics_to_industry(df: pd.DataFrame, naics_col='naics', industry_col='industry') -> pd.DataFrame:
    """Maps 2-digit NAICS codes to BLS/BEA industries."""
    def mapper(sector):
        if pd.isna(sector) or str(sector).lower() == 'unknown':
            return 'Unmapped'
        sector = str(int(sector))[:2]  # Convert to string and get first 2 digits
        if sector in ['21', '11']:
            return 'Mining and Logging'
        elif sector == '23':
            return 'Construction'
        elif sector in ['31', '32', '33']:
            return 'Manufacturing'
        elif sector in ['42', '44', '45', '48', '49', '22']:
            return 'Trade, Transportation, and Utilities'
        elif sector == '51':
            return 'Information'
        elif sector == '52':
            return 'Finance and Insurance'
        elif sector == '53':
            return 'Real Estate and Rental and Leasing'
        elif sector in ['54', '55', '56']:
            return 'Professional and Business Services'
        elif sector == '61':
            return 'Private Education Services'
        elif sector == '62':
            return 'Health Care and Social Assistance'
        elif sector in ['71', '72']:
            return 'Leisure and Hospitality'
        elif sector == '81':
            return 'Other Services'
        elif sector == '92':
            return 'Government'
        else:
            return 'Unknown Industry'
    df = df.copy()
    df[industry_col] = df[naics_col].apply(mapper)
    print('NAICS mapped to BLS/BEA industries.')
    return df


# BEA industry mapping
def map_bea_industries(df: pd.DataFrame, column: str = 'description') -> pd.DataFrame:
    """Map BEA industry descriptions to standardized industry categories consistent with BLS/WVSOS classifications."""
    bea_mapping = {
        # Top level total
        'all industry total': 'Total Nonfarm',
        # Mining / Logging
        'farms': 'Mining and Logging',
        'forestry, fishing, and related activities': 'Mining and Logging',
        'oil and gas extraction': 'Mining and Logging',
        'mining (except oil and gas)': 'Mining and Logging',
        'support activities for mining': 'Mining and Logging',
        # Trade / Transportation / Utilities
        'utilities': 'Trade, Transportation, and Utilities',
        'wholesale trade': 'Trade, Transportation, and Utilities',
        'retail trade': 'Trade, Transportation, and Utilities',
        'transportation and warehousing': 'Trade, Transportation, and Utilities',
        # Construction
        'construction': 'Construction',
        # Manufacturing
        'manufacturing': 'Manufacturing',
        # Information
        'information': 'Information',
        # Finance / Insurance
        'finance and insurance': 'Finance and Insurance',
        # Real Estate / Rental / Leasing
        'real estate': 'Real Estate and Rental and Leasing',
        'rental and leasing services and lessors of nonfinancial intangible assets': 'Real Estate and Rental and Leasing',
        # Professional / Business Services
        'professional, scientific, and technical services': 'Professional and Business Services',
        'management of companies and enterprises': 'Professional and Business Services',
        'administrative and support and waste management and remediation services': 'Professional and Business Services',
        # Educational Services
        'educational services': 'Private Educational Services',
        # Health Care / Social Assistance
        'health care and social assistance': 'Health Care and Social Assistance',
        # Leisure / Hospitality
        'arts, entertainment, and recreation': 'Leisure and Hospitality',
        'accommodation and food services': 'Leisure and Hospitality',
        # Other Services
        'other services (except government and government enterprises)': 'Other Services',
        # Government
        'government and government enterprises': 'Government',
    }

    # Normalize text
    df[column] = df[column].str.strip().str.lower()

    # Apply mapping
    df['industry'] = df[column].map(bea_mapping).fillna('Other / Unknown')
    print(f"Mapped {len(bea_mapping)} BEA industries to standardized categories.")
    return df


# Save CSV Standardized
def save_csv(df: pd.DataFrame, path) -> None:
    """Saves dataframe to CSV with standardized settings."""
    df.to_csv(path, **CSV_EXPORT_KWARGS)


# Cumulative Active Calculation
def calculate_active_orgs(yearly_df: pd.DataFrame) -> pd.DataFrame:
    """Calculates cumulative active organizations: active = cumulative filings - cumulative terminations"""

    df = yearly_df.copy()
    df['active_orgs'] = df['new_filings'].cumsum() - df['terminations'].cumsum()
    return df