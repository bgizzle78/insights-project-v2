# Imports
import pandas as pd
from src.database.db_connection import get_engine
from src.data_pipeline.load.load_utils import load_dataframe_to_table

# Load WVSOS
def load_wvsos():
    """Loads WVSOS yearly filings data into PostgreSQL."""

    engine = get_engine()

    file_path = '../insights-project-v2/data/final/wvsos_final_yearly.csv'
    df = pd.read_csv(file_path)

    print('\n📊 WVSOS Preview:')
    print(df.head())

    load_dataframe_to_table(
        df=df,
        table_name='wvsos_yearly',
        engine=engine,
        if_exists='replace'
    )

# Run script
if __name__ == '__main__':
    load_wvsos()