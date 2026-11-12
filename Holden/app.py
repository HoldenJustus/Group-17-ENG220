
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

# --------------------------------------------------
# Page setup
# --------------------------------------------------

st.set_page_config(
    page_title="Cuba, NM Transportation",
    page_icon="🚗",
    layout="wide"
)

DATA_FOLDER = Path(__file__).parent

st.title("Transportation in Cuba, New Mexico")
st.write(
    "An overview of transportation methods, "
    "commute times, and household vehicle availability."
)

st.caption(
    "Source: U.S. Census Bureau, 2020–2024 "
    "American Community Survey 5-Year Estimates."
)

# --------------------------------------------------
# Load CSV files created by MATLAB
# --------------------------------------------------

@st.cache_data
def load_data(filename):
    file_path = DATA_FOLDER / filename

    if not file_path.exists():
        return None

    data = pd.read_csv(file_path)

    # Remove MATLAB/Pandas index columns if present
    data = data.loc[
        :, ~data.columns.str.contains("^Unnamed")
    ]

    required = [
        "Label",
        "Count",
        "Percent",
        "PercentMOE",
        "Reliability",
        "TotalBase"
    ]

    if not all(column in data.columns for column in required):
        raise ValueError(
            f"{filename} is missing one or more required columns."
        )

    for column in ["Count", "Percent", "PercentMOE", "TotalBase"]:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

    return data


try:
    modes = load_data("modes.csv")
    times = load_data("time.csv")
    vehicles = load_data("vehicles.csv")

    missing = [
        name for name, data in [
            ("modes.csv", modes),
            ("time.csv", times),
            ("vehicles.csv", vehicles)
        ]
        if data is None
    ]

    if missing:
        st.error(
            "The following CSV files could not be found: "
            + ", ".join(missing)
        )
        st.info(
            "Place all three CSV files in the same folder "
            "as app.py, then rerun the app."
        )
        st.stop()

except Exception as error:
    st.error(f"Unable to load the project data: {error}")
    st.stop()


# --------------------------------------------------
# Summary information
# --------------------------------------------------

st.subheader("Transportation overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Workers",
    f"{int(modes['TotalBase'].iloc[0])}"
)

col2.metric(
    "Commuting workers",
    f"{int(times['TotalBase'].iloc[0])}"
)

col3.metric(
    "Households",
    f"{int(vehicles['TotalBase'].iloc[0])}"
)

st.divider()


# --------------------------------------------------
# Reusable graph function
# --------------------------------------------------

def show_graph(data, title, description):

    st.subheader(title)
    st.write(description)

    # Calculate the margin-of-error boundaries
    chart_data = data.copy()

    chart_data["Lower"] = (
        chart_data["Percent"] - chart_data["PercentMOE"]
    ).clip(lower=0)

    chart_data["Upper"] = (
        chart_data["Percent"] + chart_data["PercentMOE"]
    ).clip(upper=100)

    # Horizontal bar chart
    bars = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X(
            "Percent:Q",
            title="Percent (%)",
            scale=alt.Scale(domain=[0, 100])
        ),
        y=alt.Y(
            "Label:N",
            title=None,
            sort=None
        ),
        tooltip=[
            alt.Tooltip("Label:N", title="Category"),
            alt.Tooltip("Count:Q", title="Estimated count"),
            alt.Tooltip(
                "Percent:Q",
                title="Percent",
                format=".1f"
            ),
            alt.Tooltip(
                "PercentMOE:Q",
                title="Margin of error",
                format=".1f"
            ),
            alt.Tooltip("Reliability:N"),
        ]
    )

    # Margin-of-error lines
    errors = alt.Chart(chart_data).mark_rule(
        color="black",
        strokeWidth=2
    ).encode(
        x="Lower:Q",
        x2="Upper:Q",
        y=alt.Y("Label:N", sort=None)
    )

    chart = (
        bars + errors
    ).properties(
        height=max(250, len(chart_data) * 38)
    )

    st.altair_chart(chart, use_container_width=True)

    st.caption(
        "Black lines show the estimated margins of error. "
        "These indicate uncertainty in the Census estimates."
    )

    with st.expander("View the underlying data"):
        st.dataframe(
            data[
                [
                    "Label",
                    "Count",
                    "Percent",
                    "PercentMOE",
                    "Reliability"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )

    st.divider()


# --------------------------------------------------
# Graph 1: Transportation methods
# --------------------------------------------------

show_graph(
    modes,
    "1. Transportation Methods Used by Workers",
    "How workers in Cuba, New Mexico, travel to work."
)


# --------------------------------------------------
# Graph 2: Travel time
# --------------------------------------------------

show_graph(
    times,
    "2. Travel Time to Work",
    "Estimated commute times for workers who travel to work. "
    "People working from home are excluded."
)


# --------------------------------------------------
# Graph 3: Household vehicles
# --------------------------------------------------

show_graph(
    vehicles,
    "3. Vehicles Available per Household",
    "The estimated number of vehicles available "
    "to each household."
)


# --------------------------------------------------
# Data limitations
# --------------------------------------------------

st.subheader("Understanding the Data")

st.warning(
    "These figures are American Community Survey estimates, "
    "not exact counts. Margins of error and reliability "
    "ratings should be considered when interpreting the graphs."
)

st.write(
    "The Census data describes commuting methods, travel times, "
    "and household vehicle availability. It does not directly "
    "measure road conditions, fuel availability, vehicle "
    "breakdowns, or public transportation reliability."
)

st.caption(
    "Cuba, New Mexico | Transportation and Peace Engineering"
)
