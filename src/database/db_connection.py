# Imports
from sqlalchemy import create_engine

# PostgreSQL connection config
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'wv_insights'


# Create SQLAlchemy engine
def get_engine():
    """Creates and returns a SQLAlchemy engine for PostgreSQL connection. This engine will be reused across all ETL load scripts."""

    connection_string = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(connection_string)
    return engine