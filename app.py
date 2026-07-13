import streamlit as st

from utils.data_loader import load_clean_data
from utils.metrics import dashboard_metrics, top_goal_scorers
from utils.styles import load_css
from utils.charts import league_chart, position_chart

# -----------------

st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide"
)

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

st.markdown(load_css(), unsafe_allow_html=True)

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

col1, col2, col3, col4 = st.columns(4)

cards = [
    ("👤", "Players", metrics["players"], "Total Registered Players", "#3B82F6"),
    ("🏟", "Clubs", metrics["clubs"], "Professional Clubs", "#10B981"),
    ("🌍", "Leagues", metrics["leagues"], "Top European Leagues", "#8B5CF6"),
    ("⚽", "Goals", metrics["goals"], "Goals Scored", "#F59E0B"),
]

for col, (icon, title, value, desc, color) in zip(
    [col1, col2, col3, col4],
    cards
):
    card_html = f"""
    <div class="metric-card" style="border-top:5px solid {color};">
        <div class="metric-title">{icon} {title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-description">{desc}</div>
    </div>
    """

    with col:
        st.markdown(card_html, unsafe_allow_html=True)

# ---------------- Chart ----------------

fig = league_chart(filtered_df)

left, right = st.columns([2, 1])

with left:
    st.plotly_chart(
        league_chart(filtered_df),
        use_container_width=True
    )

with right:
    st.plotly_chart(
        position_chart(filtered_df),
        use_container_width=True
    )

st.divider()

st.subheader("🏆 Top 10 Goal Scorers")

top_players = top_goal_scorers(filtered_df)

st.dataframe(
    top_players,
    use_container_width=True,
    hide_index=False
)