# Imports
import pandas as pd
from pathlib import Path

# Constants (file paths)
BASE_DIR = Path(__file__).resolve().parents[2]

BLS_EMPLOYMENT_CLEAN_PATH = BASE_DIR / 'data' / 'processed' / 'processed_bls_employment.csv'
BLS_UNEMPLOYMENT_CLEAN_PATH = BASE_DIR / 'data' / 'processed' / 'processed_bls_unemployment.csv'

BLS_EMPLOYMENT_FINAL_PATH = BASE_DIR / 'data' / 'final' / 'bls_employment_by_industry.csv'
BLS_UNEMPLOYMENT_FINAL_PATH = BASE_DIR / 'data' / 'final' / 'bls_unemployment_summary.csv'

# Function: load_data(filepath)
def load_data(filepath: Path) -> pd.DataFrame:
    """Loads cleaned data"""
    try:
        df = pd.read_csv(filepath, parse_dates=['date'])
        print(f'Loaded {len(df)} rows from {filepath}')
        return df
    except FileNotFoundError:
        print(f'File not found: {filepath}')
        raise


# Function: map_series_to_industry (series id -> industry name)
def map_series_to_industry(df: pd.DataFrame) -> pd.DataFrame:
    """Replace series_id with human-readable industry names (YOU will define the mapping dictionary)"""
    df = df.copy()

    series_map = {
    'SMU54000000000000001': 'Total Nonfarm',
    'SMU54000001000000001': 'Mining and Logging',
    'SMU54000002000000001': 'Construction',
    'SMU54000003000000001': 'Manufacturing',
    'SMU54000004000000001': 'Trade, Transportation, and Utilities',
    'SMU54000005000000001': 'Information',
    'SMU54000005552000001': 'Finance and Insurance',
    'SMU54000005553000001': 'Real Estate and Rental and Leasing',
    'SMU54000006000000001': 'Professional and Business Services',
    'SMU54000006561000001': 'Private Educational Services',
    'SMU54000006562000001': 'Health Care and Social Assistance',
    'SMU54000007000000001': 'Leisure and Hospitality',
    'SMU54000008000000001': 'Other Services',
    'SMU54000009000000001': 'Government'
}

    df['industry'] = df['series_id'].map(series_map)

    print(df[['series_id', 'industry']].drop_duplicates())

    return df

# Function: filter_relevant_data
def filter_relevant_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter to relevant geography, seasonal adjustment, etc.
    """
    df = df.copy()

    # TODO: Add filters if needed
    return df

# Function: aggregate_employment
def aggregate_employment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate employment data for analysis
    """
    df = df.copy()

    # TODO: Example:
    # group by industry + date
    # df = df.groupby(['industry', 'date'])['value'].mean().reset_index()

    return df

# Function: aggregate_unemployment
def aggregate_unemployment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate unemployment data
    """
    df = df.copy()

    # TODO: Example:
    # df = df.groupby('date')['value'].mean().reset_index()

    return df


# Function: save_data
def save_data(df: pd.DataFrame, output_path: Path):
    """Save transformed data"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f'Saved data to {output_path}')


# Main Function: transform_bls_employment
def transform_bls_employment():
    df = load_data(BLS_EMPLOYMENT_CLEAN_PATH)

    df = map_series_to_industry(df)
    df = filter_relevant_data(df)
    df = aggregate_employment(df)

    save_data(df, BLS_EMPLOYMENT_FINAL_PATH)

# Main Function: transform_bls_unemployment
def transform_bls_unemployment():
    df = load_data(BLS_UNEMPLOYMENT_CLEAN_PATH)

    df = filter_relevant_data(df)
    df = aggregate_unemployment(df)

    save_data(df, BLS_UNEMPLOYMENT_FINAL_PATH)


# Run script
if __name__ == '__main__':
    print('Transforming BLS data...')

    transform_bls_employment()
    transform_bls_unemployment()

    print('Done!')