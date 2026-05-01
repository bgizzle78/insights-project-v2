# =====================================
# IMPORTS
# =====================================
import streamlit as st

# =====================================
# KPI CARD RENDER (UI HELPER)
# =====================================
def render_kpi_card(title, value, color=None):
    """Render a styled KPI card for Streamlit dashboards.
    Parameters
    ----------
    title : str
        Label displayed at the top of the card
    value : str | int | float
        Value to display (should already be formatted)
    color : str, optional
        CSS color string for the value text (e.g. '#4CAF50')"""

    color_style = f'color:{color};' if color else ''

    st.markdown(
        f'''
        <div style='background-color:#1f1f1f;padding:18px;border-radius:14px;min-height:130px;line-height:1.1;'>
            <div style='font-size:22px;opacity:0.7;'>{title}</div>
            <div style='font-size:28px;font-weight:700;margin-top:10px;{color_style}'>
                {value}
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )