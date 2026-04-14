# Imports
import pandas as pd
from src.database.db_connection import get_engine
from src.data_pipeline.load.load_utils import load_dataframe_to_table

# Load BEA
def load_bea():
    """Loads BEA GDP data into PostgreSQL."""

    engine = get_engine()

    file_path = '../insights-project-v2/data/final/bea_final.csv'
    df = pd.read_csv(file_path)

    print('\n📊 BEA GDP Preview:')
    print(df.head())

    load_dataframe_to_table(
        df=df,
        table_name='bea_gdp',
        engine=engine,
        if_exists='replace'
    )

# Run script
if __name__ == '__main__':
    load_bea()