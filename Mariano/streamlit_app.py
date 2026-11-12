
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path(__file__).parent

st.title("Transportation in Cuba, New Mexico")
st.write("ENG 220 - Transportation Data Analysis")

# Section 1: Keep the original graph
st.header("1. How Workers in Cuba Get to Work")

st.write(
    "I used 2024 Census data and MATLAB to analyze "
    "how workers in Cuba travel to work."
)

st.image(str(folder / "Cuba_Transportation copy.png"))

st.write(
    "76.3% drive alone, 5.3% carpool, "
    "2.2% walk, and 16.2% work from home. "
    "The Census estimate shows 0% using public "
    "transportation to commute."
)

# Section 2: Cleaner bus timeline
st.header("2. Limited Public Transportation")

st.write(
    "Rio Metro Route 8 - departures from "
    "Cuba Municipal Complex"
)

fig, ax = plt.subplots(figsize=(9, 2.5))

ax.plot([8.3167, 15.5], [0, 0],
        color="#B65D4B", linewidth=4)

ax.scatter([8.3167, 15.5], [0, 0],
           color="#334155", s=110, zorder=3)

ax.text(8.3167, 0.18, "8:19 AM",
        ha="center", fontsize=12)

ax.text(15.5, 0.18, "3:30 PM",
        ha="center", fontsize=12)

ax.text(11.9, -0.22, "7 hours, 11 minutes apart",
        ha="center", fontsize=13,
        color="#B65D4B", fontweight="bold")

ax.set_xlim(7.5, 16.3)
ax.set_ylim(-0.5, 0.5)
ax.axis("off")

st.pyplot(fig)
plt.close(fig)

st.write(
    "With a large gap between these scheduled "
    "departures, residents may have fewer options "
    "for traveling at different times of the day."
)

# Section 3: Wildlife collision graph
st.header("3. Wildlife Collisions on US 550")

st.write("Reported collisions on US 550, mileposts 64-80")

animals = ["Elk", "Deer", "Black Bear"]
collisions = [120, 82, 5]

fig, ax = plt.subplots(figsize=(8, 4))

bars = ax.bar(animals, collisions, color="#C65D45")

for bar, value in zip(bars, collisions):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        str(value),
        ha="center",
        fontsize=12
    )

ax.set_ylim(0, 140)
ax.set_ylabel("Reported collisions")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

st.pyplot(fig)
plt.close(fig)

st.subheader("208 reported collisions")

st.write(
    "Wildlife collisions can cause vehicle damage, "
    "safety risks, and possible road delays."
)

st.write(
    "Wildlife crossings and fencing are being "
    "considered to improve safety on this highway."
)

st.caption(
    "The three bars show 207 collisions. "
    "One additional mountain lion collision "
    "is not shown."
)

# Sources
st.header("Sources")

st.markdown(
    "[U.S. Census Bureau - ACS 2024]"
    "(https://censusreporter.org/)"
)

st.markdown(
    "[Rio Metro - Route 8]"
    "(https://www.riometro.org/DocumentCenter/View/92)"
)

st.markdown(
    "[NMDOT - US 550 Wildlife Project]"
    "(https://www.dot.nm.gov/projects/active-projects/us550wildlifeproject/)"
)
