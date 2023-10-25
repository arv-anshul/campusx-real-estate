import pandas as pd
import streamlit as st

from src.core.errors import DataValidationError
from src.data import validate
from src.data.cleaner import DataCleaner
from src.property.entity import ALL_PROPERTY
from src.typing import stop as _stop

st.set_page_config("Add new city", "🏙️", "wide", "expanded")
st_msg = st.empty()
st.header(":blue[Add new city into dataset]", divider="blue")

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
for i, prop in enumerate(ALL_PROPERTY.values(), 1):
    prop_df = prop.extract_this_property(df)
    prop.dump_dataframe(prop_df, "user", extend)

# --- --- Uploaded dataset summary --- --- #
st.header("📊 :red[Dataset Summary]", divider="red")

l, m1, m2, r = st.columns(4)
l.metric(":blue[**Shape of data**]", str(df.shape))
m1.metric(":blue[**No. of Cities**]", df["CITY"].nunique())
m2.metric(":blue[**No. of PropertyTypes**]", df["PROPERTY_TYPE"].nunique())

st.write(f":blue[**Columns:**] `{df.columns.tolist()}`")

l, r = st.columns(2)
# Insights about CITY column
l.subheader(":blue[Insights about Cities]", divider="blue")
grp_by_city = df.groupby("CITY")
l.dataframe(
    (
        grp_by_city.aggregate(
            {
                "PROP_ID": "count",
                "PRICE": "mean",
                "AREA": "mean",
            }
        )
        .astype(int)
        .sort_values("PROP_ID", ascending=False)
    ),
    use_container_width=True,
    height=178,
)

# Insights about PROPERTY_TYPE column
r.subheader(":blue[Insights about PropertyTypes]", divider="blue")
grp_by_prop_type = df.groupby("PROPERTY_TYPE")
r.dataframe(
    (
        grp_by_prop_type.aggregate(
            {
                "PROP_ID": "count",
                "PRICE": "mean",
                "AREA": "mean",
            }
        )
        .astype(int)
        .sort_values("PROP_ID", ascending=False)
    ),
    use_container_width=True,
)

st.link_button(
    "**Click For More Insights**",
    "/Analytics_Page",
    use_container_width=True,
)
