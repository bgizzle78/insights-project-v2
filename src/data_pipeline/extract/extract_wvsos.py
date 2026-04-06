# Imports
import pandas as pd
from src.config import WVSOS_RAW_PATH, WVSOS_PROCESSED_PATH
from src.utils import clean_column_names, parse_dates, save_csv


# Load Raw Data
def load_wvsos_data():
    """Load the raw WVSOS CSV file."""
    try:
        df = pd.read_csv(WVSOS_RAW_PATH)
        print(f'Loaded {len(df)} rows from {WVSOS_RAW_PATH}')
        return df
    except FileNotFoundError:
        print(f'File not found: {WVSOS_RAW_PATH}')
        raise


# Select Relevant Columns
def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only relevant columns for analysis."""
    columns = [
        'Organization Name',
        'Org Type',
        'Filing Date',
        'Termination Date',
        'Business Purpose',
        'NAICS',
        'Charter State'
    ]

    df = df[columns]
    print(f'Selected relevant columns: {len(columns)} columns remaining')
    return df


# Clean Data
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names and parse date columns."""
    # Standardize column names
    df = clean_column_names(df)
    print('Standardized column names')

    # Convert dates
    df = parse_dates(df, ['filing_date', 'termination_date'])
    print('Converted filing_date and termination_date to datetime')

    # Print null counts for awareness
    print('Missing filing_date:', df['filing_date'].isna().sum())
    print('Missing termination_date:', df['termination_date'].isna().sum())
    return df


# Save Processed Data
def save_processed_data(df: pd.DataFrame):
    """Save the processed WVSOS dataset."""
    save_csv(df, WVSOS_PROCESSED_PATH)
    print(f'Saved processed data to {WVSOS_PROCESSED_PATH}')


# Main Pipeline
def main():
    print('Starting WVSOS extract pipeline...\n')
    df = load_wvsos_data()
    df = select_columns(df)
    df = clean_data(df)
    save_processed_data(df)
    print('\nWVSOS extract step complete. Processed data saved.')


# Run Script
if __name__ == '__main__':
    main()