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

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# ⚙️ Configuration for Analysis
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
st.header(":red[⚙️ Configuration for Analysis]", divider="red")
city: str = st.selectbox(
    "🌇 Select City",
    options=(_ := prop_df["CITY"].unique()),
    format_func=lambda x: x.title(),
    disabled=True if len(_) == 1 else False,
)  # type: ignore

st.divider()

# --- --- Filter and Update Dataset --- --- #
prop_df = prop_df.query("CITY==@city")
prop_df["PRICE_PER_SQFT"] = prop_df["PRICE"].div(prop_df["AREA"])

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Visualizations with Plotly Mapbox
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
st.subheader(
    f":blue[Average price of {st_pages.decorate_options(prop_type)} by locality in {city.title()}]",
    divider="blue",
)

mapbox_bhk: int | None = None
if prop_type != "res_land":
    mapbox_bhk = st.selectbox(
        "Select BHK",
        options=[0] + sorted(prop_df["BEDROOM_NUM"].unique().tolist()),
        format_func=lambda x: f"{int(x)} BHK".replace("99", "5+").replace(
            "0 BHK", "Overall"
        ),
    )  # type: ignore


@st.cache_data
def get_df_for_scatter_map(df: pd.DataFrame, mapbox_bhk: int | None) -> pd.DataFrame:
    filter_with_bhk = df.query("BEDROOM_NUM==@mapbox_bhk") if mapbox_bhk else df

    curr_df = filter_with_bhk.groupby("LOCALITY_NAME")[
        ["AREA", "PRICE", "PRICE_PER_SQFT", "LATITUDE", "LONGITUDE"]
    ].mean()

    curr_df[["AREA", "PRICE", "PRICE_PER_SQFT"]] = curr_df[
        ["AREA", "PRICE", "PRICE_PER_SQFT"]
    ].astype(int)
    return curr_df


curr_df = get_df_for_scatter_map(prop_df, mapbox_bhk)
with st.expander("👀 See the data used to make the scatter map."):
    st.dataframe(curr_df.sort_values("PRICE"), use_container_width=True)


@st.cache_data
def plot_scatter_mapbox(df: pd.DataFrame) -> Figure:
    fig = px.scatter_mapbox(
        data_frame=df,
        lat="LATITUDE",
        lon="LONGITUDE",
        color_continuous_scale=px.colors.cyclical.IceFire,
        hover_name=curr_df.index.str.title(),
        center=st_pages.get_center_lat_lon(curr_df),
        opacity=0.7,
        zoom=10,
        height=700,
        color="PRICE",
        hover_data=["AREA", "PRICE_PER_SQFT"],
        mapbox_style="open-street-map",
    )
    fig.update_traces(marker_size=12)
    return fig


st.plotly_chart(plot_scatter_mapbox(curr_df), True)


# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Optimized Functions
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
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
# Insights Plots on BHK Sector-Wise
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
if prop_type == "res_land":
    st.info(f"No BHK comparison for {st_pages.decorate_options(prop_type)}", icon="🥹")
    _stop()

st.subheader(
    f":blue[🏘️ BHK Insights of {city.title()} City Sector-Wise]", divider="blue"
)

locality: str = st.selectbox(
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
curr_df["BEDROOM_NUM"] = curr_df["BEDROOM_NUM"].replace(99, "More than 5")

curr_df = (
    curr_df.groupby("BEDROOM_NUM")[["PRICE", "AREA", "PRICE_PER_SQFT"]]
    .mean()
    .astype(int)
)

with st.expander("👀 See the data used to make below plot."):
    st.dataframe(curr_df.T, use_container_width=True)

_ = st.columns([0.35, 0.7])[-1].radio(
    "Choose Comparison Value",
    options=["PRICE_PER_SQFT", "AREA", "PRICE"],
    horizontal=True,
    label_visibility="collapsed",
)
fig = plot_bar(
    curr_df,
    x=curr_df.index.tolist(),
    y=_,
    labels={"x": "BEDROOM_NUM"},
)
st.plotly_chart(fig, True)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Regression graph with Scatter-Plot
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
st.subheader(
    f"📈 :blue[Plot Distributions of Different Parameters of {city.title()} City]",
    divider="blue",
)

color_ = st.radio(
    "Select Third Parameter (COLOR)",
    options=[
        None,
        "BEDROOM_NUM",
        "FLOOR_NUM",
        "LUXURY_CATEGORY",
    ],
    horizontal=True,
)

x_ = st.radio(
    "Select X-axis Value",
    options=[
        "AREA",
        "PRICE_PER_SQFT",
    ],
    horizontal=True,
)

fig = plot_scatter(prop_df, x=x_, y="PRICE", color=color_, hover_name="PROP_ID")
st.plotly_chart(fig, True)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Range Visualizations with Box-Plot
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
st.subheader(
    f"🧐 :blue[Visualize Ranges of PRICE and AREA in {city.title()} City]",
    divider="blue",
)
x_ = st.radio(
    "Select X-axis Values",
    options=[
        None,
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
