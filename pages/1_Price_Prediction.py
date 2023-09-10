import streamlit as st

from src.core.constants import ALL_PROPERTY
from src.property import utils as prop_utils
from src.typing import PropertyAlias
from src.utils import st_pages

st.set_page_config("Price Prediction", "🏘️", "centered", "expanded")
st.write(st.session_state)
st_msg = st.empty()

st.title("Real Estate Price Prediction")


prop_type: PropertyAlias = st.radio(
    "Select Property Type",
    options=list(ALL_PROPERTY.keys()),
    format_func=st_pages.decorate_options,
    key="PROPERTY_TYPE",
    horizontal=True,
    label_visibility="collapsed",
)  # type: ignore

selected_property = ALL_PROPERTY[prop_type]

# Show streamlit form according to selected prop_type
with st.form("predictor_form"):
    try:
        selected_property.st_form()

        if st.form_submit_button():
            st.toast("Form Submitted!", icon="🌟")
            prop_utils.is_valid_locality_selected()
            df = prop_utils.get_df_from_session_state(selected_property)
        else:
            st.stop()

    except ValueError as e:
        st.toast("Got an Error!", icon="😵‍💫")
        st_msg.error(e, icon="🔥")
        st.stop()

st.write(df)
