# =============================
# transform_wvsos.py - streamlined
# =============================

# Imports
import pandas as pd
from src.config import WVSOS_PROCESSED_PATH, WVSOS_FINAL_PATH, START_YEAR, END_YEAR, STANDARD_INDUSTRIES
from src.utils import filter_year_range, add_year_columns, fill_unknown, save_csv, map_naics_to_industry

# Load processed data
def load_processed_data() -> pd.DataFrame:
    """Load the processed WVSOS CSV file."""
    try:
        df = pd.read_csv(WVSOS_PROCESSED_PATH, parse_dates=['filing_date', 'termination_date'])
        print(f'Loaded {len(df)} rows from {WVSOS_PROCESSED_PATH}')
        return df
    except FileNotFoundError:
        print(f'File not found: {WVSOS_PROCESSED_PATH}')
        raise

# Clean / Filter Data
def filter_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Filter by year range, remove unwanted org types, and standardize missing values."""
    df = filter_year_range(df, 'filing_date', START_YEAR, END_YEAR)
    df = df[df['org_type'] != 'TMO | Trademark Holder']
    df = fill_unknown(df, ['org_type', 'charter_state', 'business_purpose'])
    df['naics'] = df['naics'].fillna('unknown')
    return df

# Extract Year Columns
def add_year_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Add filing_year and termination_year columns."""
    df = add_year_columns(df, {'filing_date': 'filing_year', 'termination_date': 'termination_year'})
    return df

# Map WVSOS NAICS to BLS industries
def map_industries(df: pd.DataFrame) -> pd.DataFrame:
    """Map NAICS codes to BLS/BEA industry categories."""
    df = map_naics_to_industry(df, naics_col='naics', industry_col='industry')
     # Rename unmapped rows to 'Unknown Industry'
    df['industry'] = df['industry'].replace({'Unmapped': 'Unknown Industry'})
    return df

# Aggregate yearly metrics
def aggregate_yearly(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate filings, terminations, and active orgs by year and industry."""
    # New filings
    filings = df.groupby(['filing_year', 'industry']).size().rename('new_filings').reset_index()
    # Terminations
    terminations = (
        df.dropna(subset=['termination_year'])
          .groupby(['termination_year', 'industry'])
          .size()
          .rename('terminations')
          .reset_index()
    )
    # Build full year-industry grid from STANDARD_INDUSTRIES
    industries_to_include = [i for i in STANDARD_INDUSTRIES if i in df['industry'].values]
    if 'Unknown Industry' in df['industry'].values:
        industries_to_include.append('Unknown Industry')  # keep unmapped rows

    years = range(START_YEAR, END_YEAR + 1)
    grid = pd.MultiIndex.from_product([years, industries_to_include], names=['year','industry']).to_frame(index=False)

    # Merge filings and terminations
    yearly_df = grid.merge(filings, left_on=['year','industry'], right_on=['filing_year','industry'], how='left')
    yearly_df = yearly_df.merge(terminations, left_on=['year','industry'], right_on=['termination_year','industry'], how='left')

    # Clean up
    yearly_df = yearly_df.drop(columns=['filing_year','termination_year'])
    yearly_df = yearly_df.fillna(0)
    yearly_df['new_filings'] = yearly_df['new_filings'].astype(int)
    yearly_df['terminations'] = yearly_df['terminations'].astype(int)
    return yearly_df

# Save final data
def save_final(yearly_df: pd.DataFrame):
    save_path = WVSOS_FINAL_PATH.with_name(WVSOS_FINAL_PATH.stem + '_yearly.csv')
    save_csv(yearly_df, save_path)
    print(f'Final WVSOS yearly data saved to {save_path}')

# Main pipeline
def main():
    print('Starting WVSOS transform pipeline...\n')
    df = load_processed_data()
    df = filter_and_clean(df)
    df = add_year_cols(df)
    df = map_industries(df)
    yearly_df = aggregate_yearly(df)
    save_final(yearly_df)
    print('\nWVSOS transform complete! Ready for PostgreSQL.')

# Run script
if __name__ == '__main__':
    main()