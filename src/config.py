# Imports
from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Paths
DATA_DIR = BASE_DIR / 'data'

RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
FINAL_DATA_DIR = DATA_DIR / 'final'

# WVSOS File Paths
WVSOS_RAW_PATH = RAW_DATA_DIR / 'WVSOS Business Registrations Complete Data -Needs Cleaning.csv'
WVSOS_PROCESSED_PATH = PROCESSED_DATA_DIR / 'processed_wvsos.csv'
WVSOS_FINAL_PATH = FINAL_DATA_DIR / 'wvsos_final.csv'

# BEA File Paths
BEA_RAW_PATH = RAW_DATA_DIR / 'SAGDP9_WV_1997_2024.csv'
BEA_PROCESSED_PATH = PROCESSED_DATA_DIR / 'processed_bea.csv'
BEA_FINAL_PATH = FINAL_DATA_DIR / 'bea_final.csv'

# Global Settings
START_YEAR = 2006
END_YEAR = 2025

# Export Settings
CSV_EXPORT_KWARGS = {
    'index': False,
    'encoding': 'utf-8'
}

# Canonical Industry List
STANDARD_INDUSTRIES = [
    'Mining and Logging',
    'Construction',
    'Manufacturing',
    'Trade, Transportation, and Utilities',
    'Information',
    'Finance and Insurance',
    'Real Estate and Rental and Leasing',
    'Professional and Business Services',
    'Private Educational Services',
    'Health Care and Social Assistance',
    'Leisure and Hospitality',
    'Other Services',
    'Government'
]