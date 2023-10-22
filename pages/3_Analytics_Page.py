from warnings import filterwarnings

import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.graph_objects import Figure

from src.core import io
from src.property import _utils as prop_utils
from src.property.entity import ALL_PROPERTY
from src.typing import DatasetType, PropertyAlias
from src.typing import stop as _stop
from src.utils import st_pages

filterwarnings("ignore", category=UserWarning)

st.set_page_config("Analytics Page", "🗺️", "wide", "expanded")

st_msg = st.container()

dataset_type: DatasetType = st.sidebar.selectbox(
    "Choose the model for prediction",
    options=["main", "user"],
    format_func=lambda x: x.capitalize(),
    help="This is used to select the model for prediction.",
    key="DatasetType",
)  # type: ignore

prop_type: PropertyAlias = st.sidebar.radio(
    "Select Property Type",
    options=list(ALL_PROPERTY.keys()),
    format_func=st_pages.decorate_options,
    key="PROPERTY_TYPE",
)  # type: ignore

selected_property = ALL_PROPERTY[prop_type]

try:
    prop_df = io.read_csv(
        prop_utils.get_dataset_path(selected_property.prop_type, dataset_type)
    )
except FileNotFoundError:
    st.columns([0.1, 0.8, 0.1])[1].image(
        "https://indianmemetemplates.com/wp-content/uploads/Bhai-kya-kar-raha-hai-tu.jpg",
        caption="Upload your data!!",
    )
    st.info("User data not found. Upload your data [here](/Add_New_City).", icon="💢")
    st.toast("Data upload kar bhai!", icon="🤦")
    _stop()

prop_df["PRICE_PER_SQFT"] = prop_df["PRICE"].div(prop_df["AREA"])

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Visualizations in Maps
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
exp1 = st.expander("**🗺️ Visualizations in Maps**", expanded=True)

exp1.columns([0.3, 0.6])[-1].radio(
    "Select Map Style",
    options=["open-street-map", "carto-positron"],
    format_func=lambda x: x.replace("-", " ").title(),
    key="MAPBOX_STYLE",
    horizontal=True,
    label_visibility="collapsed",
)

exp1_tabs = exp1.tabs(
    [
        f"Average PRICE of {st_pages.decorate_options(prop_type)} (per sq.ft.)",
        f"Average PRICE of {st_pages.decorate_options(prop_type)} (by sector)",
        f"Average AREA of {st_pages.decorate_options(prop_type)} (by sector)",
    ]
)

curr_df = prop_df.groupby("LOCALITY_NAME")[
    ["AREA", "PRICE", "PRICE_PER_SQFT", "LATITUDE", "LONGITUDE"]
].mean()
curr_df[["AREA", "PRICE", "PRICE_PER_SQFT"]] = curr_df[
    ["AREA", "PRICE", "PRICE_PER_SQFT"]
].round(2)


def plot_scatter_mapbox(color: str, hover_data: list[str], **kwargs) -> Figure:
    kwargs_for_scatter_mapbox: dict = dict(
        data_frame=curr_df,
        lat="LATITUDE",
        lon="LONGITUDE",
        color_continuous_scale=px.colors.cyclical.IceFire,
        hover_name=curr_df.index.str.title(),
        center=st_pages.get_center_lat_lon(curr_df),
        opacity=0.5,
        zoom=10,
        height=700,
        **kwargs,
    )

    fig = px.scatter_mapbox(
        color=color,
        hover_data=hover_data,
        **kwargs_for_scatter_mapbox,
    )
    fig.update_traces(marker_size=12)
    return fig


with exp1_tabs[0]:
    fig = plot_scatter_mapbox(
        color="PRICE_PER_SQFT",
        hover_data=["AREA", "PRICE"],
        mapbox_style=st.session_state["MAPBOX_STYLE"],
    )
    st.plotly_chart(fig, True)

with exp1_tabs[1]:
    fig = plot_scatter_mapbox(
        color="AREA",
        hover_data=["PRICE_PER_SQFT", "PRICE"],
        mapbox_style=st.session_state["MAPBOX_STYLE"],
    )
    st.plotly_chart(fig, True)

with exp1_tabs[2]:
    fig = plot_scatter_mapbox(
        color="PRICE",
        hover_data=["PRICE_PER_SQFT", "AREA"],
        mapbox_style=st.session_state["MAPBOX_STYLE"],
    )
    st.plotly_chart(fig, True)


# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Optimized Functions
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
@st.cache_data
def plot_pie(df: pd.DataFrame, names: str | None, **kwargs) -> Figure:
    fig = px.pie(df, names=names, **kwargs)
    return fig


@st.cache_data
def plot_bar(df: pd.DataFrame, x: list[str], y: str | None, **kwargs) -> Figure:
    fig = px.bar(df, x=x, y=y, **kwargs)
    return fig


@st.cache_data
def plot_scatter(
    df: pd.DataFrame,
    x: str | None,
    y: str | None,
    color: str | None,
    hover_name: str | None,
    **kwargs,
) -> Figure:
    fig = px.scatter(df, x=x, y=y, color=color, hover_name=hover_name, **kwargs)
    return fig


@st.cache_data
def plot_box(df: pd.DataFrame, x: str | None, y: str | None, **kwargs) -> Figure:
    fig = px.box(df, x=x, y=y, **kwargs)
    return fig


# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Basic Insights Plots
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
if prop_type == "res_land":
    st.info(f"No BHK comparison for {st_pages.decorate_options(prop_type)}", icon="🥹")
    _stop()

exp2 = st.expander("**🧠 Basic Insights Plots**", expanded=True)

locality: str = exp2.selectbox(
    "Select Sector",
    options=["Overall"] + prop_df["LOCALITY_NAME"].sort_values().unique().tolist(),
    format_func=lambda x: x.title(),
    key="LOCALITY_NAME",
)  # type: ignore
curr_df = (
    prop_df
    if locality == "Overall"
    else prop_df.query("LOCALITY_NAME==@locality").copy()
)

exp2_tabs = exp2.tabs(
    [
        "BHK Count",
        "Insights on BHK",
    ]
)

with exp2_tabs[0]:
    curr_df["BEDROOM_NUM"] = curr_df["BEDROOM_NUM"].apply(prop_utils.format_99_option)
    fig = plot_pie(curr_df, names="BEDROOM_NUM")
    st.plotly_chart(fig, True)


with exp2_tabs[1]:
    curr_data = (
        curr_df.groupby("BEDROOM_NUM")[["PRICE", "AREA", "PRICE_PER_SQFT"]]
        .mean()
        .round(2)
    )
    _ = st.columns([0.35, 0.7])[-1].radio(
        "Choose Comparison Value",
        options=["PRICE_PER_SQFT", "AREA", "PRICE"],
        horizontal=True,
        label_visibility="collapsed",
    )
    fig = plot_bar(curr_data, x=curr_data.index.tolist(), y=_)
    st.plotly_chart(fig, True)
    st.dataframe(curr_data.T, use_container_width=True)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# More Visualizations
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
exp3 = st.expander("**💭 Insights on AREA, PRICE and PRICE_PER_SQFT**", expanded=True)
exp3_tabs = exp3.tabs(
    [
        "AREA vs PRICE vs PRICE_PER_SQFT",
        "Visualize Ranges",
    ]
)

with exp3_tabs[0]:
    color_ = st.radio(
        "Select third parameter (color)",
        options=[
            None,
            "BEDROOM_NUM",
            "FLOOR_NUM",
            "LUXURY_CATEGORY",
        ],
        horizontal=True,
    )

    x_ = st.radio(
        "Select X-axis value",
        options=[
            "AREA",
            "PRICE_PER_SQFT",
        ],
        horizontal=True,
    )

    fig = plot_scatter(prop_df, x=x_, y="PRICE", color=color_, hover_name=color_)
    st.plotly_chart(fig, True)

with exp3_tabs[1]:
    x_ = st.radio(
        "Select X-axis Values",
        options=[
            "BEDROOM_NUM",
            "FLOOR_NUM",
            "LUXURY_CATEGORY",
        ],
        horizontal=True,
    )

    y_ = st.radio(
        "Select Y-axis Values",
        options=[
            "PRICE",
            "AREA",
            "PRICE_PER_SQFT",
        ],
        horizontal=True,
    )

    fig = plot_box(prop_df, x=x_, y=y_)
    st.plotly_chart(fig, True)
