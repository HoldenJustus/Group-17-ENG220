"""
ENG 220 Team 17 - Transportation in Cuba, NM
Streamlit app: upload the commute data (CSV or the downloaded .zip) and it
detects which dataset it is and makes the graphs.

  - "Commuter Transportation.csv"  -> how people get to work (2013-2024)
  - "Commute Time.csv"             -> how long the commute takes (Cuba vs. US)

If nothing is uploaded, the app uses the copies in the data/ folder (if any).

Run locally:   streamlit run app.py
"""

import io
import zipfile
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"

st.set_page_config(page_title="Cuba, NM Commuting", layout="wide")

# Midpoint (minutes) of each travel-time range, used to estimate the average.
# "90+ Minutes" has no upper limit, so 100 minutes is assumed.
MIDPOINTS = {0: 2.5, 1: 7, 2: 12, 3: 17, 4: 22, 5: 27, 6: 32,
             7: 37, 8: 42, 9: 52, 10: 74.5, 11: 100}
BROAD_GROUP = {0: "Under 15 min", 1: "Under 15 min", 2: "Under 15 min",
               3: "15-29 min", 4: "15-29 min", 5: "15-29 min",
               6: "30-44 min", 7: "30-44 min", 8: "30-44 min",
               9: "45-59 min", 10: "60+ min", 11: "60+ min"}
BROAD_ORDER = ["Under 15 min", "15-29 min", "30-44 min", "45-59 min", "60+ min"]


# --------------------------------------------------------------------------
# Loading uploaded files (CSV or ZIP) and detecting the dataset type
# --------------------------------------------------------------------------
def read_uploads(files):
    """Return a list of (name, DataFrame) from uploaded CSV/ZIP files."""
    out = []
    for f in files:
        try:
            data = f.getvalue()
            if f.name.lower().endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    for member in z.namelist():
                        if member.lower().endswith(".csv") and not member.startswith("__MACOSX"):
                            out.append((Path(member).name, pd.read_csv(z.open(member))))
            else:
                out.append((f.name, pd.read_csv(io.BytesIO(data))))
        except Exception as e:  # bad zip, not a CSV, etc.
            st.warning(f"Could not read **{f.name}**: {e}")
    return out


def detect(df):
    if "Commute Means" in df.columns:
        return "transportation"
    if "Travel Time" in df.columns:
        return "time"
    return None


# --------------------------------------------------------------------------
# Dataset 1: Commuter Transportation
# --------------------------------------------------------------------------
def show_transportation(raw, key):
    df = raw.rename(columns={"Group ID": "GroupID", "Commute Means": "Workers",
                             "Commute Means Moe": "MOE", "share": "Share"})
    df["SharePct"] = df["Share"] * 100
    df = df.sort_values(["GroupID", "Year"])

    years = sorted(df["Year"].unique())
    group_order = df.drop_duplicates("GroupID").sort_values("GroupID")["Group"].tolist()
    totals_by_group = df.groupby("Group")["Workers"].sum()
    active = [g for g in group_order if totals_by_group[g] > 0]   # skip always-0 types

    c1, c2 = st.columns([2, 1])
    chosen = c1.multiselect("Commute types", active, default=active, key=f"{key}_types")
    if len(years) > 1:
        yr_range = c2.slider("Years", int(years[0]), int(years[-1]),
                             (int(years[0]), int(years[-1])), key=f"{key}_years")
    else:
        yr_range = (int(years[0]), int(years[0]))
    show_moe = st.checkbox("Show margin of error", key=f"{key}_moe")

    sub = df[df["Group"].isin(chosen) & df["Year"].between(*yr_range)]
    in_range = df[df["Year"].between(*yr_range)]

    latest = df[df["Year"] == yr_range[1]]
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Total workers ({yr_range[1]})", int(latest["Workers"].sum()))
    for col, grp in ((m2, "Drove Alone"), (m3, "Worked At Home")):
        v = latest.loc[latest["Group"] == grp, "SharePct"]
        col.metric(f"{grp} ({yr_range[1]})", f"{v.iloc[0]:.1f}%" if len(v) else "n/a")

    st.subheader("Workers by commute type (bar graph)")
    fig = px.bar(sub, x="Year", y="Workers", color="Group", barmode="group",
                 error_y="MOE" if show_moe else None,
                 category_orders={"Group": group_order},
                 labels={"Workers": "Number of workers"})
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_bar")

    st.subheader("Workers by commute type over time")
    fig = px.line(sub, x="Year", y="Workers", color="Group", markers=True,
                  error_y="MOE" if show_moe else None,
                  category_orders={"Group": group_order},
                  labels={"Workers": "Number of workers"})
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_line")

    st.subheader("Share of workers by commute type")
    fig = px.bar(sub, x="Year", y="SharePct", color="Group", barmode="stack",
                 category_orders={"Group": group_order},
                 labels={"SharePct": "Share of workers (%)"})
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_stack")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Average workers per type")
        avg = (sub.groupby("Group", as_index=False)["Workers"].mean()
               .sort_values("Workers", ascending=False))
        fig = px.bar(avg, x="Group", y="Workers", text_auto=".1f",
                     labels={"Workers": "Average workers"})
        st.plotly_chart(fig, use_container_width=True, key=f"{key}_avg")
    with c2:
        st.subheader("Average share over the period")
        avg_share = sub.groupby("Group", as_index=False)["Share"].mean()
        fig = px.pie(avg_share[avg_share["Share"] > 0], names="Group", values="Share")
        st.plotly_chart(fig, use_container_width=True, key=f"{key}_pie")

    st.subheader("Total workers per year")
    totals = in_range.groupby("Year", as_index=False)["Workers"].sum()
    fig = px.bar(totals, x="Year", y="Workers", text_auto=True,
                 labels={"Workers": "Total workers"})
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_total")

    with st.expander("Show data table"):
        wide = df.pivot(index="Year", columns="Group", values="Workers")[group_order]
        wide["Total"] = wide.sum(axis=1)
        st.dataframe(wide, use_container_width=True)


# --------------------------------------------------------------------------
# Dataset 2: Commute Time
# --------------------------------------------------------------------------
def show_commute_time(raw, key):
    df = raw.rename(columns={"Travel Time ID": "TimeID", "Travel Time": "TravelTime",
                             "Commuter Population": "Commuters",
                             "Commuter Population Moe": "MOE", "share": "Share"})
    df["SharePct"] = df["Share"] * 100

    year_list = sorted(df["Year"].unique())
    year = st.selectbox("Year", year_list[::-1], key=f"{key}_year") if len(year_list) > 1 \
        else int(year_list[0])
    ct = df[df["Year"] == year].sort_values(["Place", "TimeID"]).copy()
    places = ct["Place"].unique().tolist()
    bin_order = ct.drop_duplicates("TimeID").sort_values("TimeID")["TravelTime"].tolist()

    # Estimated average commute per place
    ct["Mid"] = ct["TimeID"].map(MIDPOINTS)
    ct["MinXPeople"] = ct["Mid"] * ct["Commuters"]
    summary = ct.groupby("Place").agg(Total=("Commuters", "sum"),
                                      MinXPeople=("MinXPeople", "sum"))
    summary["AvgMinutes"] = summary["MinXPeople"] / summary["Total"]

    cols = st.columns(len(places))
    for col, place in zip(cols, places):
        col.metric(f"Est. average commute: {place}",
                   f"{summary.loc[place, 'AvgMinutes']:.1f} min",
                   help="Uses the middle of each range; assumes 100 min for '90+'.")

    st.subheader(f"Travel time to work, {year} (share of commuters)")
    fig = px.bar(ct, x="TravelTime", y="SharePct", color="Place", barmode="group",
                 category_orders={"TravelTime": bin_order},
                 labels={"SharePct": "Share of commuters (%)", "TravelTime": "Travel time"})
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_share")

    st.subheader("Number of commuters by travel time")
    default = places.index("Cuba, NM") if "Cuba, NM" in places else 0
    place = st.selectbox("Place", places, index=default, key=f"{key}_place")
    one = ct[ct["Place"] == place]
    fig = go.Figure(go.Bar(
        x=one["TravelTime"], y=one["Commuters"],
        error_y=dict(type="data", symmetric=False, array=one["MOE"],
                     arrayminus=one[["MOE", "Commuters"]].min(axis=1)),  # stop at 0
    ))
    fig.update_layout(xaxis_title="Travel time", yaxis_title="Number of commuters",
                      title=f"{place}, {year} (error bars = margin of error)")
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_counts")

    st.subheader("Broad commute groups")
    ct["Broad"] = ct["TimeID"].map(BROAD_GROUP)
    broad = ct.groupby(["Place", "Broad"], as_index=False)["SharePct"].sum()
    fig = px.bar(broad, x="Broad", y="SharePct", color="Place", barmode="group",
                 text_auto=".1f", category_orders={"Broad": BROAD_ORDER},
                 labels={"SharePct": "Share of commuters (%)", "Broad": ""})
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_broad")

    st.subheader("Cumulative share: % who get to work within X minutes")
    ct["CumPct"] = ct.groupby("Place")["SharePct"].cumsum()
    fig = px.line(ct, x="TravelTime", y="CumPct", color="Place", markers=True,
                  category_orders={"TravelTime": bin_order},
                  labels={"CumPct": "Cumulative share (%)", "TravelTime": "Travel time"})
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_cum")

    st.subheader("Estimated average commute time")
    avg = summary.reset_index()
    fig = px.bar(avg, x="Place", y="AvgMinutes", text_auto=".1f",
                 labels={"AvgMinutes": "Estimated average (minutes)", "Place": ""})
    st.plotly_chart(fig, use_container_width=True, key=f"{key}_avg")

    with st.expander("Show data table"):
        wide = ct.pivot(index="TravelTime", columns="Place", values="SharePct").loc[bin_order]
        st.dataframe(wide.round(1), use_container_width=True)


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------
st.title("Commuting in Cuba, NM")
st.caption("Source: U.S. Census Bureau American Community Survey (ACS), via Data USA.")

uploads = st.file_uploader(
    "Upload commute data: 'Commuter Transportation.csv', 'Commute Time.csv', or the .zip downloads",
    type=["csv", "zip"], accept_multiple_files=True)

if uploads:
    datasets = read_uploads(uploads)
else:
    datasets = [(p.name, pd.read_csv(p)) for p in sorted(DATA_DIR.glob("*.csv"))]
    if datasets:
        st.info("Showing the data saved with the app. Upload files above to use your own.")
    else:
        st.info("Upload a CSV or ZIP file to get started.")
        st.stop()

recognized = [(name, df, detect(df)) for name, df in datasets]
for name, _, kind in recognized:
    if kind is None:
        st.warning(f"Skipped **{name}**: not a recognized commute dataset.")
recognized = [r for r in recognized if r[2] is not None]
if not recognized:
    st.stop()

titles = {"transportation": "How people get to work", "time": "How long the commute takes"}
tabs = st.tabs([f"{titles[kind]} ({Path(name).stem})" for name, _, kind in recognized])
for i, (tab, (name, df, kind)) in enumerate(zip(tabs, recognized)):
    with tab:
        if kind == "transportation":
            show_transportation(df, key=f"t{i}")
        else:
            show_commute_time(df, key=f"c{i}")
        st.download_button("Download this data (CSV)", df.to_csv(index=False),
                           Path(name).name, "text/csv", key=f"dl{i}")
