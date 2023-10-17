import pandas as pd
import streamlit as st

from src.core.errors import DataValidationError
from src.database import validate
from src.database.cleaner import DataCleaner
from src.property.entity import ALL_PROPERTY
from src.typing import stop as _stop
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
    extend = st.checkbox("Extend with existing data.", value=True)

    if not st.form_submit_button(use_container_width=True):
        _stop()

if uploaded is None:
    st.toast("Something went wrong!", icon="😵‍💫")
    st_msg.error("Uploaded file is gives None to streamlit.")
    _stop()

df = pd.read_csv(uploaded)


# Validate the user's dataset for further progress
try:
    validate.validate_dataset(df)
except DataValidationError as e:
    st.toast("Something went wrong!", icon="😵‍💫")
    st_msg.error(e, icon="🔥")
    _stop()

# Clean the dataset with step first cleaning
with st.spinner("Your Dataset is Cleaning..."):
    cleaner = DataCleaner(df)
    df = cleaner.initiate()

st.toast("Your dataset is cleaned.", icon="🤓")

# Split dataset into different properties
progress_text = "Splitting the dataset into different properties..."
with st.progress(0, progress_text):
    total = len(ALL_PROPERTY)

    for i, prop in enumerate(ALL_PROPERTY.values(), 1):
        prop_df = prop.extract_this_property(df)
        prop.dump_dataframe(prop_df, "user", extend)

        st.progress(i / total, progress_text)

# --- --- Uploaded dataset summary --- --- #
tab1, tab2 = st.tabs(["🗃️ Show Dataset", "📈 Dataset Summary"])

with tab1:
    st.dataframe(df.sample(100).reset_index(drop=True))
    st.info("Showing a sample of your dataset. (100 rows)", icon="👀")

with tab2:
    st.warning("Cooking a function to show the summary of your dataset.", icon="🧑‍🍳")
