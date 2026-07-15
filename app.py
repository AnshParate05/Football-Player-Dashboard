import streamlit as st

from utils.data_loader import load_clean_data
from utils.metrics import (
    dashboard_metrics,
    top_goal_scorers,
    top_assist_providers
)
from utils.styles import load_css
from utils.charts import (
    league_chart,
    position_chart
)

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide"
)

# ----------------------------------------------------
# Load CSS
# ----------------------------------------------------

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

df = load_clean_data()

# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------

st.sidebar.title("⚽ Analytics Filters")

league = st.sidebar.selectbox(
    "🌍 League Filter",
    ["All"] + sorted(df["Comp"].unique())
)

club = st.sidebar.selectbox(
    "🏟 Club Filter",
    ["All"] + sorted(df["Squad"].unique())
)

position = st.sidebar.selectbox(
    "⚽ Position Filter",
    ["All"] + sorted(df["Pos"].unique())
)

age = st.sidebar.slider(
    "👤 Age Range",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(
        int(df["Age"].min()),
        int(df["Age"].max())
    )
)

# ----------------------------------------------------
# Apply Filters
# ----------------------------------------------------

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

# ----------------------------------------------------
# Dashboard Metrics
# ----------------------------------------------------

metrics = dashboard_metrics(filtered_df)

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.title("⚽ Football Analytics Dashboard")

st.caption(
    "Professional Football Player Analytics • Top 5 European Leagues • Season 2025–26"
)

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

cards = [
    ("👤", "Players", metrics["players"], "Total Registered Players", "#3B82F6"),
    ("🏟", "Clubs", metrics["clubs"], "Professional Clubs", "#10B981"),
    ("🌍", "Leagues", metrics["leagues"], "Top European Leagues", "#8B5CF6"),
    ("⚽", "Goals", metrics["goals"], "Goals Scored", "#F59E0B"),
]

for column, (icon, title, value, desc, color) in zip(
    [col1, col2, col3, col4],
    cards
):

    with column:

        st.markdown(
            f"""
<div class="metric-card" style="border-top:5px solid {color};">
    <div class="metric-title">{icon} {title}</div>
    <div class="metric-value">{value}</div>
    <div class="metric-description">{desc}</div>
</div>
""",
            unsafe_allow_html=True
        )
# ----------------------------------------------------
# League Analytics
# ----------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 📊 League Analytics", unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:

    st.plotly_chart(
    league_chart(filtered_df),
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)

with right:

    st.plotly_chart(
    position_chart(filtered_df),
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)

# ----------------------------------------------------
# Player Leaderboards
# ----------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## 🏆 Player Leaderboards", unsafe_allow_html=True)

left, right = st.columns(2)

with left:

    st.subheader("🏆 Top 10 Goal Scorers")

    st.dataframe(
        top_goal_scorers(filtered_df),
        use_container_width=True
    )

with right:

    st.subheader("🎯 Top 10 Assist Providers")

    st.dataframe(
        top_assist_providers(filtered_df),
        use_container_width=True
    )

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.divider()

st.markdown(
    """
<div style="
text-align:center;
color:#9CA3AF;
font-size:14px;
padding:10px 0;
">

⚽ <b>Football Analytics Dashboard</b> |
Developed by <b>Ansh Parate</b> |
Version 1.0 |
FBref 2025–26 Dataset |
Streamlit • Plotly • Pandas

</div>
""",
    unsafe_allow_html=True
)