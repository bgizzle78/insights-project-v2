# Imports
import pandas as pd
from pathlib import Path
from typing import Tuple
from src.config import WVSOS_PROCESSED_PATH, WVSOS_FINAL_PATH, START_YEAR, END_YEAR
from src.utils import filter_year_range, add_year_columns, fill_unknown, save_csv, calculate_active_orgs, map_naics_to_industry

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
    """Filter by year range and remove unwanted org types."""
    df = filter_year_range(df, 'filing_date', START_YEAR, END_YEAR)
    print(f'Filtered to years {START_YEAR}-{END_YEAR}, {len(df)} rows remain')
    
    # Remove TMO | Trademark Holder
    df = df[df['org_type'] != 'TMO | Trademark Holder']
    print(f'Filtered out TMO org_type, {len(df)} rows remain')

    # Fill unknown categories
    df = fill_unknown(df, ['org_type', 'charter_state', 'business_purpose'])
    print('Filled unknown categorical fields')

    # Ensure NAICS has consistent unknown values
    df['naics'] = df['naics'].fillna('unknown')
    print('Standardized NAICS missing values to unknown')
    return df


# Extract Year Columns
def add_year_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Add filing_year and termination_year columns."""
    df = add_year_columns(df, {'filing_date': 'filing_year', 'termination_date': 'termination_year'})
    print('Added filing_year and termination_year columns')
    return df


# Map NAICS to WVSOS Industries
def map_industries(df: pd.DataFrame) -> pd.DataFrame:
    """Map NAICS codes to BLS/BEA industry categories."""
    df = map_naics_to_industry(df, naics_col='naics', industry_col='industry')
    print('Mapped NAICS codes to industries')

    # QA check
    unmapped_count = (df['industry'] == 'Unknown Industry').sum()
    print(f"Unknown industries: {unmapped_count}")
    return df

# Aggregate yearly metrics
def aggregate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    print('Aggregating yearly metrics...')

    # Filings per year
    filings = df.groupby('filing_year').size().rename('new_filings').reset_index()

    # Terminations per year
    terminations = (
        df.dropna(subset=['termination_year'])
          .groupby('termination_year')
          .size()
          .rename('terminations')
          .reset_index()
    )

    # Create full year range
    yearly_df = pd.DataFrame({'year': range(START_YEAR, END_YEAR + 1)})

    # Merge filings and terminations onto full year range
    yearly_df = yearly_df.merge(filings, left_on='year', right_on='filing_year', how='left')
    yearly_df = yearly_df.merge(terminations, left_on='year', right_on='termination_year', how='left')

    # Clean up columns
    yearly_df = yearly_df.drop(columns=['filing_year', 'termination_year'])
    yearly_df = yearly_df.fillna(0)

    # Ensure integer types
    yearly_df['new_filings'] = yearly_df['new_filings'].astype(int)
    yearly_df['terminations'] = yearly_df['terminations'].astype(int)

    # Calculate cumulative active orgs
    yearly_df = calculate_active_orgs(yearly_df)

    print('Yearly metrics aggregated.')
    return yearly_df

# Industry and Org Type breakdown
def breakdown_by_category(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    print('Aggregating industry and org_type breakdowns...')
    # Keep unknown for metrics but exclude for visuals
    industry_breakdown = (
    df[df['industry'] != 'Unknown Industry']
    .groupby('industry')
    .size()
    .rename('count')
    .reset_index()
)
    orgtype_breakdown = df.groupby('org_type').size().rename('count').reset_index()
    return industry_breakdown, orgtype_breakdown

# Save final outputs
def save_final_data(yearly_df: pd.DataFrame, industry_df: pd.DataFrame, orgtype_df: pd.DataFrame):
    print('Saving final CSV outputs...')
    yearly_path = WVSOS_FINAL_PATH.with_name(WVSOS_FINAL_PATH.stem + '_yearly.csv')
    industry_path = WVSOS_FINAL_PATH.with_name(WVSOS_FINAL_PATH.stem + '_industry.csv')
    orgtype_path = WVSOS_FINAL_PATH.with_name(WVSOS_FINAL_PATH.stem + '_orgtype.csv')

    save_csv(yearly_df, yearly_path)
    save_csv(industry_df, industry_path)
    save_csv(orgtype_df, orgtype_path)
    print('Final WVSOS data saved.')

# Main pipeline
def main():
    print('Starting WVSOS transform pipeline...\n')
    df = load_processed_data()
    df = filter_and_clean(df)
    df = add_year_cols(df)
    df = map_industries(df)
    yearly_df = aggregate_metrics(df)
    industry_df, orgtype_df = breakdown_by_category(df)
    save_final_data(yearly_df, industry_df, orgtype_df)
    print('\nWVSOS transform complete! Ready for dashboards/SQL.')

# Run script
if __name__ == '__main__':
    main()