import streamlit as st

from src.property import _utils as prop_utils
from src.property.entity import ALL_PROPERTY
from src.property.form_options import form_options
from src.typing import PropertyAlias
from src.utils import st_pages

st.set_page_config("Price Prediction", "🏘️", "centered", "expanded")
st_msg = st.empty()

prop_type: PropertyAlias = st.sidebar.radio(
    "Select Property Type",
    options=list(ALL_PROPERTY.keys()),
    format_func=st_pages.decorate_options,
    key="PROPERTY_TYPE",
    horizontal=True,
    label_visibility="collapsed",
)  # type: ignore

selected_property = ALL_PROPERTY[prop_type]

st.subheader(st_pages.colorizer(st_pages.decorate_options(prop_type), "green"), divider="green")
st.selectbox("Select City", options=["Select ..."] + form_options.CITY, key="CITY")

if st.session_state["CITY"] != "Select ...":
    st.selectbox(
        "Select Locality",
        options=form_options.LOCALITY_NAME(st.session_state["CITY"]),
        key="LOCALITY_NAME",
    )
else:
    st.stop()

# Show streamlit form according to selected prop_type
with st.form("predictor_form"):
    try:
        selected_property.st_form()

        if st.form_submit_button():
            st.toast("Form Submitted!", icon="🌟")
            df = prop_utils.get_df_from_session_state(selected_property)
        else:
            st.stop()

    except ValueError as e:
        st.toast("Got an Error!", icon="😵‍💫")
        st_msg.error(e, icon="🔥")
        st.stop()

st.write(df)
