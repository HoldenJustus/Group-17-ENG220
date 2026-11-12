

import streamlit as st
from pathlib import Path

# Find the folder containing this Python file
folder = Path(__file__).parent

# Website title
st.title("Transportation in Cuba, New Mexico")
st.write("ENG 220 - Transportation Data Analysis")

# Section 1: Census Transportation Data
st.header("1. How Workers in Cuba Get to Work")

st.write(
    "I used 2024 Census data and MATLAB to analyze "
    "how workers in Cuba travel to work."
)

st.image(str(folder / "Cuba_Transportation copy.png"))

st.write(
    "76.3% of workers drive alone, 5.3% carpool, "
    "2.2% walk, and 16.2% work from home. "
    "The Census estimate shows 0% commuting "
    "using public transportation."
)

# Section 2: Public Transportation
st.header("2. Limited Public Transportation")

st.write(
    "I analyzed the Rio Metro Route 8 bus schedule "
    "using MATLAB."
)

st.image(str(folder / "Cuba_Bus_Timeline.png"))

st.write(
    "The two scheduled departures from the Cuba "
    "Municipal Complex are 8:19 AM and 3:30 PM. "
    "That is a gap of 7 hours and 11 minutes."
)

# Section 3: Wildlife Collisions
st.header("3. Wildlife Collisions on US 550")

st.write(
    "NMDOT reported 208 wildlife-vehicle collisions "
    "along a section of US 550 near Cuba."
)

st.write(
    "These collisions can create safety risks, "
    "vehicle damage, and possible road delays. "
    "Wildlife crossings and fencing could help "
    "reduce collisions."
)

# Sources
st.header("Sources")

st.write("U.S. Census Bureau - ACS 2024, Table B08006")
st.write("Rio Metro Regional Transit District - Route 8")
st.write("New Mexico Department of Transportation - US 550")
