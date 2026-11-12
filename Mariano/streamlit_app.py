
import streamlit as st
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(
    page_title="Transportation in Cuba, New Mexico",
    layout="wide"
)

st.title("Transportation in Cuba, New Mexico")
st.write("ENG 220 - Transportation and Road Conditions")

# ==========================================
# SECTION 1: ROAD CONDITIONS
# ==========================================

st.header("1. When the Weather Turns, the Roads Close")

st.write(
    "Weather can make traveling difficult for people living "
    "in and around Cuba, New Mexico."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💧 Mud & Washouts")
    st.write(
        "Residents told the Sandoval County Commission (2021) "
        "that reservation roads were bladed but still not passable, "
        "blocking trips to the doctor and grocery store."
    )

with col2:
    st.subheader("❄️ Snow & Ice")
    st.write(
        "Cuba Independent School District has switched to remote "
        "days because of dangerous road conditions after winter storms."
    )

with col3:
    st.subheader("🚌 School Buses on Dirt")
    st.write(
        "Bus routes run from asphalt to gravel to deeply rutted dirt, "
        "with homes a mile or two apart along the route."
    )

st.caption(
    "Sources: Sandoval County Commission public comment "
    "(Sept 2021); KRQE; AP / PBS NewsHour (Oct 2020)"
)

st.divider()

# ==========================================
# SECTION 2: PUBLIC TRANSPORTATION
# ==========================================

st.header("2. Limited Public Transportation in Cuba")

st.write(
    "I analyzed the Rio Metro Route 8 bus schedule using MATLAB."
)

st.subheader(
    "Rio Metro Route 8 - Departures from Cuba Municipal Complex"
)

# Bus departure times in 24-hour format
morning = 8 + 19 / 60
afternoon = 15 + 30 / 60

fig, ax = plt.subplots(figsize=(10, 3))

ax.plot(
    [morning, afternoon],
    [1, 1],
    color="#B65F4B",
    linewidth=4
)

ax.scatter(
    [morning, afternoon],
    [1, 1],
    color="#34495E",
    s=150,
    zorder=3
)

ax.text(
    morning, 1.12, "8:19 AM",
    ha="center", fontsize=12
)

ax.text(
    afternoon, 1.12, "3:30 PM",
    ha="center", fontsize=12
)

ax.text(
    (morning + afternoon) / 2,
    0.83,
    "7 hours, 11 minutes apart",
    ha="center",
    fontsize=13,
    color="#B65F4B",
    fontweight="bold"
)

ax.set_xlim(7, 17)
ax.set_ylim(0.6, 1.4)
ax.set_yticks([])
ax.set_xticks([8, 10, 12, 14, 16])
ax.set_xticklabels(
    ["8 AM", "10 AM", "12 PM", "2 PM", "4 PM"]
)
ax.set_xlabel("Time of Day")

for spine in ax.spines.values():
    spine.set_visible(False)

st.pyplot(fig)
plt.close(fig)

st.write(
    "The two scheduled departures from the Cuba Municipal "
    "Complex are 8:19 AM and 3:30 PM. That is a gap of "
    "7 hours and 11 minutes between these departures."
)

st.write(
    "This large gap may make it harder for residents "
    "to travel at different times of the day."
)

st.caption(
    "Source: Rio Metro Regional Transit District - Route 8"
)

st.divider()

# ==========================================
# SECTION 3: WILDLIFE COLLISIONS
# ==========================================

st.header("3. Wildlife Collisions on US 550")

st.write(
    "NMDOT reported 208 wildlife-vehicle collisions "
    "along a section of US 550 near Cuba."
)

st.subheader("Reported Wildlife Collisions on US 550")

animals = ["Elk", "Deer", "Black Bear"]
collisions = [120, 82, 5]

fig2, ax2 = plt.subplots(figsize=(9, 4))

bars = ax2.bar(
    animals,
    collisions,
    color="#B65F4B",
    width=0.55
)

for bar in bars:
    height = bar.get_height()
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        height + 2,
        str(int(height)),
        ha="center",
        fontsize=12
    )

ax2.set_ylabel("Reported Collisions")
ax2.set_ylim(0, 140)
ax2.set_title("US 550 - Wildlife-Vehicle Collisions")

st.pyplot(fig2)
plt.close(fig2)

st.write(
    "Wildlife collisions can cause vehicle damage, "
    "safety risks, and possible road delays."
)

st.write(
    "Wildlife crossings and fencing are being considered "
    "to improve safety on this highway."
)

st.caption(
    "Sources: NMDOT presentation to NM Legislature "
    "(Sept 2024); NM Wildlife Corridors Action Plan (2022). "
    "The three displayed categories total 207; "
    "the cited overall figure is 208."
)

st.divider()

# ==========================================
# SOURCES
# ==========================================

st.header("Sources")

st.markdown(
    """
- Sandoval County Commission public comment (Sept 2021)
- KRQE; AP / PBS NewsHour (Oct 2020)
- [Rio Metro Route 8 Schedule](https://www.riometro.org/DocumentCenter/View/92)
- [NMDOT US 550 Wildlife Project](https://www.dot.nm.gov/projects/active-projects/us550wildlifeproject/)
- NM Wildlife Corridors Action Plan (2022)
"""
)
