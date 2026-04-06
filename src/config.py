# Imports
from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Paths
DATA_DIR = BASE_DIR / 'data'

RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
FINAL_DATA_DIR = DATA_DIR / 'final'

# File Paths
WVSOS_RAW_PATH = RAW_DATA_DIR / 'WVSOS Business Registrations Complete Data -Needs Cleaning.csv'
WVSOS_PROCESSED_PATH = PROCESSED_DATA_DIR / 'wvsos_processed.csv'
WVSOS_FINAL_PATH = FINAL_DATA_DIR / 'wvsos_final.csv'

# Global Settings
START_YEAR = 2006
END_YEAR = 2025

# Export Settings
CSV_EXPORT_KWARGS = {
    'index': False,
    'encoding': 'utf-8'
}