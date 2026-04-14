# Imports
import pandas as pd
from src.database.db_connection import get_engine
from src.data_pipeline.load.load_utils import load_dataframe_to_table

# Load BLS Unemployment
def load_bls_unemployment():
    """Loads BLS unemployment data into PostgreSQL."""

    engine = get_engine()

    file_path = '../insights-project-v2/data/final/bls_unemployment_summary.csv'
    df = pd.read_csv(file_path)

    print('\n📊 BLS Unemployment Preview:')
    print(df.head())

    load_dataframe_to_table(
        df=df,
        table_name='bls_unemployment',
        engine=engine,
        if_exists='replace'
    )

# Run script
if __name__ == '__main__':
    load_bls_unemployment()