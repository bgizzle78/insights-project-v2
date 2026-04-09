# Imports
import pandas as pd
from pathlib import Path

# Constants (file paths)
BASE_DIR = Path(__file__).resolve().parents[3]

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
    """Keep only relevant columns for analysis. (No filtering needed since data was pre-filtered upstream)"""
    df = df.copy()

    # Keep only columns needed for analysis
    columns_to_keep = [
        'series_id',
        'industry',
        'date',
        'value'
    ]

    # Only keep columns that exist (prevents errors)
    df = df[[col for col in columns_to_keep if col in df.columns]]

    # Sanity checks (no filtering)
    print(f'Unique series count: {df["series_id"].nunique()}')

    if 'industry' in df.columns:
        print(f'Industries present: {df["industry"].nunique()}')

    print(f'Date range: {df["date"].min()} to {df["date"].max()}')

    print(df.columns)
    
    print(df.head())

    return df

# Function: aggregate_employment
def aggregate_employment(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate employment data to yearly averages by industry"""
    df = df.copy()

    # Extract year from date
    df['year'] = df['date'].dt.year

    # Group and aggregate
    df = (
        df.groupby(['industry', 'year'])['value']
        .mean()
        .reset_index()
    )

    # Rename for clarity
    df = df.rename(columns={'value': 'avg_employment'})

    # Multiply by 1000 to get readable employment numbers
    df['avg_employment'] = (df['avg_employment'] * 1000).round().astype(int)

    df = df.sort_values(['industry', 'year'])

    print(df.head(10))
    print(df.columns)

    return df

# Function: aggregate_unemployment
def aggregate_unemployment(df: pd.DataFrame) -> pd.DataFrame:
    """Transform unemployment dataset into a clean, wide, yearly table:
    columns: year, unemployment_rate, labor_force_participation_rate, labor_force"""
    df = df.copy()

    # Map series_id to metric
    series_map = {
        'LASST540000000000003': 'unemployment_rate',
        'LASST540000000000008': 'labor_force_participation_rate',
        'LAUST540000000000006': 'labor_force'
    }
    df['metric'] = df['series_id'].map(series_map)

    # Extract year
    df['year'] = df['date'].dt.year

    # Pivot to wide table
    df_wide = df.pivot_table(
        index='year',
        columns='metric',
        values='value',
        aggfunc='mean'
    ).reset_index()

    # Ensure column order
    df_wide = df_wide[[
        'year', 
        'unemployment_rate', 
        'labor_force_participation_rate', 
        'labor_force'
    ]]

    # Sort by year
    df_wide = df_wide.sort_values('year')

    print(df.head(10))
    print(df.columns)

    return df_wide


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
    df = df[df['industry'] != 'Total Nonfarm']
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