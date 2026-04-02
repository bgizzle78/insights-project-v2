import pandas as pd
from pathlib import Path

# Absolute path from tests/ folder
BLS_EMPLOYMENT_CLEAN_PATH = Path('C:/Users/Newforce/workspace/insights-project-v2/data/processed/processed_bls_employment.csv')

# Load data
df = pd.read_csv(BLS_EMPLOYMENT_CLEAN_PATH, parse_dates=['date'])

# Series ID mapping
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

# Apply mapping
df['industry'] = df['series_id'].map(series_map)

# Check results
print(df[['series_id', 'industry']].drop_duplicates())