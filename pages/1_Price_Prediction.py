import pandas as pd
import streamlit as st

from src.core.errors import ModelNotFoundError
from src.property.entity import ALL_PROPERTY
from src.property.form_options import form_options
from src.property.property_type import PropertyType
from src.typing import DatasetType, PropertyAlias
from src.utils import st_pages

st.set_page_config("Price Prediction", "🏘️", "centered", "expanded")
st_msg = st.container()

st.sidebar.selectbox(
    "Choose the model for prediction",
    options=["main", "user"],
    format_func=lambda x: x.capitalize(),
    help="This is used to select the model for prediction.",
    key="DatasetType",
)
dataset_type: DatasetType = st.session_state["DatasetType"]

prop_type: PropertyAlias = st.sidebar.radio(
    "Select Property Type",
    options=list(ALL_PROPERTY.keys()),
    format_func=st_pages.decorate_options,
    key="PROPERTY_TYPE",
    horizontal=True,
    label_visibility="collapsed",
)  # type: ignore

st.subheader(st_pages.colorizer(st_pages.decorate_options(prop_type), "green"), divider="green")
selected_property = ALL_PROPERTY[prop_type]

# Button to train model of the selected property
if not selected_property.get_model_path(dataset_type, "price_predictor").exists():
    st.sidebar.button(
        "🚆 Train Model 🚆",
        use_container_width=True,
        on_click=selected_property.train_price_predictor,
        args=(dataset_type,),
        type="primary",
    )
else:
    with st.spinner("Re-Training in progress..."):
        _ = st.sidebar.button(
            "🚆 Re-Train Model 🚆",
            use_container_width=True,
        )
        if _:
            selected_property.train_price_predictor(dataset_type)
            st_msg.info("Model Re-trained successfully.", icon="🚅")


st.selectbox(
    "Select City",
    options=["Select ..."] + form_options.CITY(dataset_type, prop_type),
    key="CITY",
)

if st.session_state["CITY"] != "Select ...":
    st.selectbox(
        "Select Locality",
        options=form_options.LOCALITY_NAME(st.session_state["CITY"], dataset_type, prop_type),
        key="LOCALITY_NAME",
    )
else:
    st.stop()


def get_df_from_session_state(prop: PropertyType):
    return pd.DataFrame.from_dict(
        {k: v for k in prop.schema.ALL_COLS for i, v in st.session_state.items() if k == i},
        orient="index",
    ).T


# Show streamlit form according to selected prop_type
with st.form("predictor_form"):
    try:
        selected_property.st_form()

        if st.form_submit_button():
            st.toast("Form Submitted!", icon="🌟")
            df = get_df_from_session_state(selected_property)
        else:
            st.stop()

    except ValueError as e:
        st.toast("Got an Error!", icon="😵‍💫")
        st_msg.error(e, icon="🔥")
        st.stop()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Price Prediction
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
try:
    with st.spinner("Prediction in progress..."):
        pred_price = selected_property.predict_price(df, dataset_type)
except ModelNotFoundError as e:
    st.toast("Error Occurred!!", icon="😵‍💫")
    st_msg.error(e, icon="🤖")

    # Button to train model of the selected property
    st_msg.button(
        "🚆 Train Model 🚆",  # Applied `**` to provide unique key
        use_container_width=True,
        on_click=selected_property.train_price_predictor,
        args=(dataset_type,),
        type="secondary",
    )
    st.toast("Are you in a hurry?", icon="🚅")

    st.stop()

st.subheader(
    st_pages.colorizer(f"Prediction is {st_pages.format_price(pred_price)}"),
    divider="rainbow",
)
