"""
ENG 220 Team 17 - Commuting in Cuba, NM
Shows one graph: share of commuters by broad commute-time group,
Cuba, NM vs. the United States (same as the MATLAB graph on the slides).

Needs, next to this file:
    data/Commute Time.csv
and requirements.txt with: streamlit, pandas, numpy, matplotlib

Run locally:   streamlit run app.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

DATA_FILE = Path(__file__).parent / "data" / "Commute Time.csv"

st.set_page_config(page_title="Commutes in Cuba, NM vs. the US")
st.title("Commutes in Cuba, NM in comparison with the US")

if not DATA_FILE.exists():
    st.error("Missing file: put 'Commute Time.csv' in a 'data' folder next to app.py.")
    st.stop()

# ---- Load data -----------------------------------------------------------
T = pd.read_csv(DATA_FILE)
T.columns = ["TimeID", "TravelTime", "Year", "Commuters", "MOE",
             "Place", "PlaceID", "Share"]
yr = int(T["Year"].max())                 # most recent year
T = T[T["Year"] == yr]
places = T["Place"].unique().tolist()     # "United States", "Cuba, NM"

# ---- Combine the 12 travel-time ranges into 5 broad groups ---------------
group_labels = ["Under 15 min", "15-29 min", "30-44 min", "45-59 min", "60+ min"]
group_of = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 3, 10: 4, 11: 4}
T = T.assign(Group=T["TimeID"].map(group_of))
GroupShare = 100 * T.pivot_table(index="Group", columns="Place",
                                 values="Share", aggfunc="sum")[places]

# ---- Plot (MATLAB-style dark theme, MATLAB default colors) ---------------
colors = ["#0072BD", "#D95319"]           # MATLAB blue and orange
fig, ax = plt.subplots(figsize=(9, 5.5), facecolor="black")
ax.set_facecolor("black")

x = np.arange(len(group_labels))
width = 0.8 / len(places)
for i, p in enumerate(places):
    bars = ax.bar(x + (i - (len(places) - 1) / 2) * width, GroupShare[p], width,
                  label=p, color=colors[i % len(colors)], edgecolor="white", linewidth=0.5)
    for b in bars:
        ax.annotate(f"{b.get_height():.1f}%",
                    (b.get_x() + b.get_width() / 2, b.get_height()),
                    xytext=(0, 2), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, color="white")

ax.set_xticks(x, group_labels)
ax.set_ylabel("Share of Commuters (%)", color="white")
ax.set_title(f"Commute Time, {yr}", color="white", fontweight="bold")
ax.set_ylim(0, np.ceil(GroupShare.to_numpy().max() / 10) * 10 + 5)
ax.tick_params(colors="white")
for spine in ax.spines.values():
    spine.set_color("white")
ax.grid(True, color="gray", alpha=0.4)
ax.set_axisbelow(True)
leg = ax.legend(loc="upper right", facecolor="black", edgecolor="white")
for t in leg.get_texts():
    t.set_color("white")

st.pyplot(fig)
plt.close(fig)

st.caption(f"Source: Data USA, \"Cuba, NM,\" {yr} ACS data.")
