# =====================================
# FIX PYTHON PATH
# =====================================
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# =====================================
# IMPORTS
# =====================================
import pandas as pd
import streamlit as st
from db import run_query

# =====================================
# FUNCTIONS
# =====================================
@st.cache_data
def load_economic_data():
    """Loads economic data from the database.
    This function uses the `@st.cache_data` decorator to cache the results of the query.
    This means that the query will only be run once, and subsequent calls to this function will return the cached results.
    The function returns a Pandas DataFrame containing all columns from the `economic_master` table, sorted by the `year` column.
    Returns: pd.DataFrame: A DataFrame containing all columns from the `economic_master` table, sorted by the `year` column."""

    query = 'SELECT * FROM economic_master'
    df = run_query(query)

    # Clean + sort once
    df = df.sort_values(by=['year'])

    return df

@st.cache_data
def load_unemployment_data():
    """Loads unemployment data from the database.
    This function uses the `@st.cache_data` decorator to cache the results of the query.
    This means that the query will only be run once, and subsequent calls to this function will return the cached results.
    The function returns a Pandas DataFrame containing all columns from the `bls_unemployment` table, sorted by the `year` column.
    Returns: pd.DataFrame: A DataFrame containing all columns from the `bls_unemployment` table, sorted by the `year` column."""

    query = 'SELECT * FROM bls_unemployment'
    df = run_query(query)

    df = df.sort_values(by=['year'])

    return df