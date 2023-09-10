""" README page for Real Estate Project. """

import streamlit as st

st.set_page_config("README.md", "🗒️", "wide")

try:
    with open("README.md") as md:
        st.markdown(md.read())
except FileNotFoundError:
    st.error("README.md file not found.", icon="🔥")
