import streamlit as st

from src.property import _utils as prop_utils
from src.property.entity import ALL_PROPERTY
from src.utils import st_pages

st.set_page_config("Download Resources", "🔻", "centered", "expanded")

st.header(
    f"🔻 {st_pages.colorizer('Download Resources of this Project', 'red')}",
    divider="red",
)

st.selectbox(
    "Select **Data Type**",
    options=["main", "user"],
    format_func=lambda x: x.title(),
    key="DatasetType",
)
dataset_type = st.session_state["DatasetType"]

st.selectbox(
    "Select **ML Model**",
    options=[
        "price_predictor",
    ],
    format_func=lambda x: x.replace("_", " ").title() + " Model",
    key="ModelType",
)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
st.divider()
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #

l, r = st.columns(2, gap="medium")
l.subheader(st_pages.colorizer("Download Models", "blue"), divider="blue")
r.subheader(st_pages.colorizer("Download Datasets", "blue"), divider="blue")


for i, (prop_type_, prop) in enumerate(ALL_PROPERTY.items()):
    # Download buttons for model
    model_path = prop_utils.get_model_path(
        prop.prop_type, dataset_type, st.session_state["ModelType"]
    )

    if model_path.exists():
        with open(model_path, "rb") as model_file:
            l.download_button(
                label=st_pages.decorate_options(prop_type_),
                data=model_file,
                file_name=f"{prop_type_}_model.dill",
                use_container_width=True,
                key=f"{i}_model_enabled",
                type="primary",
            )
    else:
        l.button(
            label=st_pages.decorate_options(prop_type_),
            disabled=True,
            key=f"{i}_model_disabled",
            use_container_width=True,
        )

    # Download buttons for Dataset
    dataset_path = prop_utils.get_dataset_path(prop.prop_type, dataset_type)

    if dataset_path.exists():
        with open(dataset_path) as dataset_file:
            r.download_button(
                label=st_pages.decorate_options(prop_type_),
                data=dataset_file,
                file_name=f"{prop_type_}_dataset.csv",
                use_container_width=True,
                key=f"{i}_dataset_enabled",
                type="primary",
            )
    else:
        r.button(
            label=st_pages.decorate_options(prop_type_),
            disabled=True,
            key=f"{i}_dataset_disabled",
            use_container_width=True,
        )
