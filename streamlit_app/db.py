# =====================================
# FIX PYTHON PATH TO FIND src/
# =====================================
import sys
from pathlib import Path

# Ensure src is always visible (safe fallback)
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# =====================================
# IMPORTS
# =====================================
import pandas as pd
from src.database.db_connection import engine

# =====================================
# FUNCTIONS
# =====================================
# Run query function for streamlit app
def run_query(sql: str) -> pd.DataFrame:
    """Lightweight wrapper around SQLAlchemy engine. Keeps Streamlit clean and avoids repeating connection logic."""

    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    return df