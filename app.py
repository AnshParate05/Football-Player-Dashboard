import streamlit as st

from utils.data_loader import load_clean_data
from utils.metrics import dashboard_metrics
from utils.styles import load_css
from utils.charts import league_chart

# -----------------

st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

df = load_clean_data()

# ---------------- Sidebar ----------------

st.sidebar.title("⚙ Dashboard Settings")

theme = st.sidebar.radio(
    "Theme",
    ["🌙 Dark", "☀️ Light"]
)

league = st.sidebar.selectbox(
    "🌍 League",
    ["All"] + sorted(df["Comp"].unique().tolist())
)

club = st.sidebar.selectbox(
    "🏟 Club",
    ["All"] + sorted(df["Squad"].unique().tolist())
)

position = st.sidebar.selectbox(
    "⚽ Position",
    ["All"] + sorted(df["Pos"].unique().tolist())
)

age = st.sidebar.slider(
    "👤 Age",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(
        int(df["Age"].min()),
        int(df["Age"].max())
    )
)

# ---------------- Apply Filters ----------------

filtered_df = df.copy()

if league != "All":
    filtered_df = filtered_df[
        filtered_df["Comp"] == league
    ]

if club != "All":
    filtered_df = filtered_df[
        filtered_df["Squad"] == club
    ]

if position != "All":
    filtered_df = filtered_df[
        filtered_df["Pos"] == position
    ]

filtered_df = filtered_df[
    (filtered_df["Age"] >= age[0]) &
    (filtered_df["Age"] <= age[1])
]

metrics = dashboard_metrics(filtered_df)

st.title("⚽ Football Analytics Dashboard")

st.caption("Top 5 European Leagues 2025-26")

# ---------------- KPI ----------------

col1,col2,col3,col4 = st.columns(4)

col1.metric("Players",metrics["players"])
col2.metric("Clubs",metrics["clubs"])
col3.metric("Leagues",metrics["leagues"])
col4.metric("Goals",metrics["goals"])

# ---------------- Chart ----------------

fig = league_chart(filtered_df)

st.plotly_chart(fig,use_container_width=True)