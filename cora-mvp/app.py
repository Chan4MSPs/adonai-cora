"""
CORA - main Streamlit app launcher
Run with: streamlit run app.py
"""
import streamlit as st
import importlib
from pathlib import Path

# Initialize app path and utils
from utils import db, seed, helpers

# Ensure data directories and DB exist / seed data
db.init_db()  # creates engine and tables
seed.run_seed_if_needed()  # idempotent seed

# Simple page registry that maps display names to module path in pages/
PAGES = {
    "Dashboard": "pages.1_Dashboard",
    "Calendar": "pages.2_Calendar",
    "Create / Edit Post": "pages.3_Post_Editor",
    "AI Studio": "pages.4_AI_Studio",
    "Library": "pages.5_Library",
}

st.set_page_config(page_title="CORA — Adonai Coffee", layout="wide", initial_sidebar_state="expanded")

# App chrome
st.sidebar.image("assets/sample_images/brand_placeholder.png" if Path("assets/sample_images/brand_placeholder.png").exists() else None, width=120)
st.sidebar.title("CORA")
st.sidebar.caption("Coffee Operations + Reporting Assistant")

# Navigation
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Go to", list(PAGES.keys()), index=list(PAGES.keys()).index(st.session_state.get("page", "Dashboard")))
st.session_state["page"] = page

st.sidebar.markdown("---")
st.sidebar.markdown("CORA — Demo MVP for Adonai Coffee")
st.sidebar.markdown("Brew Hope. Fund Freedom.")

# Load and render selected page
module_name = PAGES[page]
module = importlib.import_module(module_name)
# Each page module exposes a render() function that receives nothing and uses helpers/db
module.render()