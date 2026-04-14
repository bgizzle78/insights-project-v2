# =====================================
# Fix Python path to find src/
# =====================================
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# =====================================
# IMPORTS
# =====================================
import streamlit as st

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title='WV Economic Insights',
    layout='wide'
)

# =====================================
# HOME PAGE
# =====================================
st.title('📊 West Virginia Economic Insights')

st.markdown('''
Welcome to the **WV Economic Insights Dashboard**.

### What this app does:
- Analyze employment and GDP by industry
- Track business formation and terminations
- Explore economic trends over time

### How to use:
Use the sidebar to navigate between different analysis pages.

---
Built with:
- PostgreSQL (data warehouse)
- pandas (data processing)
- Streamlit (dashboard layer)
''')