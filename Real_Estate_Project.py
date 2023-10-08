""" README page for Real Estate Project. """

from pathlib import Path

import streamlit as st

README_PATH = Path("README.md")
st.set_page_config("README.md", "📝", "wide")

try:
    st.markdown(README_PATH.read_text())
except FileNotFoundError:
    st.error("README.md file not found.", icon="🔥")
