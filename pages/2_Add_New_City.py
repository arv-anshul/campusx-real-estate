import pandas as pd
import streamlit as st

from src.core.errors import DataValidationError
from src.database.cleaner import DataCleaner
from src.utils import st_pages

st.set_page_config("Add new city", "🏙️", "wide", "expanded")
st_msg = st.empty()
st.subheader(st_pages.colorizer("Add new city into dataset", "green"), divider="green")

with st.form("add_new_city"):
    uploaded = st.file_uploader(
        "Upload New City Data",
        type=["csv"],
        label_visibility="collapsed",
    )

    if not st.form_submit_button(use_container_width=True):
        st.stop()

if uploaded is None:
    st.toast("Something went wrong!", icon="😵‍💫")
    st_msg.error("Uploaded file is gives None to streamlit.")
    st.stop()

df = pd.read_csv(uploaded)


try:
    DataCleaner.validate_dataset(df)
except DataValidationError as e:
    st.toast("Something went wrong!", icon="😵‍💫")
    st_msg.error(e, icon="🔥")
    st.stop()

with st.spinner("Your Dataset is Cleaning..."):
    cleaner = DataCleaner(df)
    df = cleaner.initiate()

st.toast("Your dataset is cleaned.", icon="🤓")

# --- --- Uploaded dataset summary --- --- #
tab1, tab2 = st.tabs(["🗃️ Show Dataset", "📈 Dataset Summary"])

with tab1:
    st.dataframe(df.sample(100).reset_index(drop=True))
    st.info("Showing a sample of your dataset. (100 rows)", icon="👀")

with tab2:
    st.warning("Cooking a function to show the summary of your dataset.", icon="🧑‍🍳")
