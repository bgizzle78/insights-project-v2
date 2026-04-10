# Imports
import pandas as pd
from sqlalchemy.engine import Engine

# Load dataframe to PostgreSQL
def load_dataframe_to_table(
    df: pd.DataFrame,
    table_name: str,
    engine: Engine,
    if_exists: str = "replace"
):
    """Loads a pandas DataFrame into a PostgreSQL table.
    Parameters:
    - df: cleaned pandas DataFrame
    - table_name: target PostgreSQL table name
    - engine: SQLAlchemy engine (from db_connection.py)
    - if_exists: default = "replace"
        - replace: drops and recreates table"""

    print(f"\n🚀 Loading {table_name} into PostgreSQL...")
    print(f"Rows: {len(df):,} | Columns: {len(df.columns)}")

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists=if_exists,
        index=False,
        chunksize=1000
    )

    print(f"✅ Successfully loaded {table_name}")