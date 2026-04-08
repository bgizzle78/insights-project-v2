# Imports
import pandas as pd
from src.config import BEA_RAW_PATH, BEA_PROCESSED_PATH, START_YEAR, END_YEAR
from src.utils import clean_column_names, save_csv


# Load Raw Data
def load_bea_data():
    """Load the raw BEA CSV file."""
    try:
        df = pd.read_csv(BEA_RAW_PATH, low_memory=False)
        print(f'Loaded {len(df)} rows from {BEA_RAW_PATH}')
        return df
    except FileNotFoundError:
        print(f'File not found: {BEA_RAW_PATH}')
        raise

# Select Relevant Columns
def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only relevant columns for analysis (WV 2006-2025)."""
    base_columns = [
        'GeoName',
        'LineCode',
        'IndustryClassification',
        'Description',
        'Unit'
    ]  

    # Only include year columns that exist in the DataFrame
    year_cols = [str(year) for year in range(START_YEAR, END_YEAR + 1) if str(year) in df.columns]
    
    columns = base_columns + year_cols
    df = df[columns]
    print(f'Selected relevant columns: {len(columns)} columns remaining')
    return df

# Clean Data
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names and prepare numeric year columns."""
    df = clean_column_names(df)
    print('Standardized column names')

    # Drop rows missing key identifiers (footnotes)
    df = df.dropna(subset=['geo_name', 'line_code', 'industry_classification', 'description'])
    print(f'Dropped rows with missing key identifiers. Remaining rows: {len(df)}')
    
    # Identify year columns that actually exist in the DataFrame
    year_cols = [col for col in df.columns if col.isdigit() and START_YEAR <= int(col) <= END_YEAR]
    
    # Convert these year columns to numeric
    for col in year_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    print(f'Converted year columns {year_cols[0]}-{year_cols[-1]} to numeric')
    
    # Print NA summary for awareness
    na_counts = df[year_cols].isna().sum()
    print('Missing values per year column:')
    print(na_counts)
    return df

# Save Processed Data
def save_processed_data(df: pd.DataFrame):
    """Save the processed BEA dataset."""
    save_csv(df, BEA_PROCESSED_PATH)
    print(f'Saved processed data to {BEA_PROCESSED_PATH}')

# Main Pipeline
def main():
    print('Starting BEA extract pipeline...\n')
    df = load_bea_data()
    df = select_columns(df)
    df = clean_data(df)
    save_processed_data(df)
    print('\nBEA extract step complete. Processed data saved.')

# Run Script
if __name__ == '__main__':
    main()