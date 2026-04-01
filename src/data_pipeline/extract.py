# Imports
import pandas as pd
from pathlib import Path

# Constants (file paths to raw and processed data)
# Project root (go up from this file -> src/data_pipeline -> project root)
BASE_DIR = Path(__file__).resolve().parents[2]

BLS_EMPLOYMENT_RAW_PATH = BASE_DIR / 'data' / 'raw' / 'bls_employment.csv'
BLS_EMPLOYMENT_PROCESSED_PATH = BASE_DIR / 'data' / 'processed' / 'processed_bls_employment.csv'

BLS_UNEMPLOYMENT_RAW_PATH = BASE_DIR / 'data' / 'raw' / 'bls_unemployment.csv'
BLS_UNEMPLOYMENT_PROCESSED_PATH = BASE_DIR / 'data' / 'processed' / 'processed_bls_unemployment.csv'

# Function: read_csv_file(filepath) -> df
def read_csv_file(filepath: Path) -> pd.DataFrame:
    """Reads a csv file into a pandas dataframe"""
    try:
        df = pd.read_csv(filepath)
        print(f'Loaded {len(df)} rows from {filepath}')
        return df
    except FileNotFoundError:
        print(f'File not found: {filepath}')
        raise

# Function: clean_bls_data(df) -> df
def clean_bls_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes column names, converts Value to numeric, ensures proper date formatting"""
    df = df.copy()

    #  Lowercase and replace spaces with underscores
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    print('Standardized column names')

    # Convert Value column to numeric
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    print('Converted Value column to numeric')

    # Convert Date column to datetime
    df['date'] = pd.to_datetime(df['label'], format='%Y-%b', errors='coerce')
    print('Converted Date column to datetime')

    # Drop rows with missing value or date
    df = df.dropna(subset=['value', 'date'])
    print('Dropped rows with missing value or date')

    return df

# Function: save_processed_data(df, output_path)
def save_processed_data(df: pd.DataFrame, output_path: Path):
    """Saves cleaned dataframe to a CSV file"""
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure folder exists
    df.to_csv(output_path, index=False)
    print(f'Saved cleaned data to {output_path}')

# # Function: generic extract function
#    - calls read -> clean -> save
#    - allows future API or other datasets to plug in
def run_extraction_pipeline(input_path: Path, output_path: Path, clean_function):
    """
    Generic extraction pipeline:
    - Reads raw data
    - Cleans it using a provided function
    - Saves processed output
    """
    print(f'\nStarting extraction for: {input_path.name}')

    df_raw = read_csv_file(input_path)
    df_clean = clean_function(df_raw)
    save_processed_data(df_clean, output_path)

    print(f'Finished processing: {input_path.name}')

# Main function: extract_bls_employment()
def extract_bls_employment():
    """Extract and process BLS employment data"""
    run_extraction_pipeline(
        input_path=BLS_EMPLOYMENT_RAW_PATH,
        output_path=BLS_EMPLOYMENT_PROCESSED_PATH,
        clean_function=clean_bls_data
    )

# Main function: extract_bls_unemployment()
def extract_bls_unemployment():
    """Extract and process BLS unemployment data"""
    run_extraction_pipeline(
        input_path=BLS_UNEMPLOYMENT_RAW_PATH,
        output_path=BLS_UNEMPLOYMENT_PROCESSED_PATH,
        clean_function=clean_bls_data
    )

# Run script
if __name__ == '__main__':
    print('Extracting BLS data...')
    extract_bls_employment()
    extract_bls_unemployment()
    print('Done!')
