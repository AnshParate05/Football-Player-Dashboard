import streamlit as st
import plotly.express as px
from io import BytesIO
from openpyxl import Workbook

from utils.data_loader import load_clean_data
from utils.styles import load_css

# -----------------------------
# Page Config
# -----------------------------
st.markdown(load_css(), unsafe_allow_html=True)

df = load_clean_data()

st.title("🌍 League Analysis")
st.caption(
    "Analyze league-wide performance, club statistics and overall trends."
)

# -----------------------------
# League Selector
# -----------------------------
league = st.selectbox(
    "Select League",
    sorted(df["Comp"].dropna().unique())
)

league_df = df[df["Comp"] == league]

# -----------------------------
# KPI Cards
# -----------------------------
total_clubs = league_df["Squad"].nunique()
total_players = league_df["Player"].nunique()
total_goals = int(league_df["Gls"].sum())
avg_age = round(league_df["Age"].mean(), 1)

cards = [
    ("🏟 Clubs", total_clubs),
    ("👥 Players", total_players),
    ("⚽ Goals", total_goals),
    ("🎂 Avg Age", avg_age),
]

cols = st.columns(4)

for col, (title, value) in zip(cols, cards):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <h5>{title}</h5>
                <h3>{value}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------
# Club Statistics
# -----------------------------
club_stats = (
    league_df.groupby("Squad")
    .agg(
        Players=("Player", "count"),
        Goals=("Gls", "sum"),
        Assists=("Ast", "sum"),
        Avg_Age=("Age", "mean"),
    )
    .reset_index()
)

# -----------------------------
# Charts
# -----------------------------
st.divider()

st.caption("Top performing clubs in the selected league")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("⚽ Top Clubs by Goals")

    top_goals = (
        club_stats.sort_values("Goals", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_goals,
        x="Goals",
        y="Squad",
        orientation="h",
        text="Goals",
        template="plotly_dark",
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Goals: %{x}<extra></extra>"
    )

    fig.update_layout(
        height=360,
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
    )

    st.plotly_chart(fig, width="stretch")


with col2:
    st.subheader("🎯 Top Clubs by Assists")

    top_assists = (
        club_stats.sort_values("Assists", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_assists,
        x="Assists",
        y="Squad",
        orientation="h",
        text="Assists",
        template="plotly_dark",
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Assists: %{x}<extra></extra>"
    )

    fig.update_layout(
        height=360,
        yaxis={"categoryorder": "total ascending"},
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
    )

    st.plotly_chart(fig, width="stretch")
# -----------------------------
# Club Statistics
# -----------------------------
st.subheader("📋 Club Statistics")

st.caption("Search, sort and explore club statistics.")

col1, col2 = st.columns([3, 1])

with col1:
    search = st.text_input(
        "🔍 Search Club",
        placeholder="Enter club name..."
    )

with col2:
    sort_by = st.selectbox(
        "Sort By",
        [
            "Goals",
            "Assists",
            "Players",
            "Average Age"
        ]
    )

display_df = club_stats.copy()

# Search filter
if search:
    display_df = display_df[
        display_df["Squad"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# Sorting
if sort_by == "Goals":
    display_df = display_df.sort_values("Goals", ascending=False)

elif sort_by == "Assists":
    display_df = display_df.sort_values("Assists", ascending=False)

elif sort_by == "Players":
    display_df = display_df.sort_values("Players", ascending=False)

else:
    display_df = display_df.sort_values("Avg_Age", ascending=False)

display_df["Avg_Age"] = display_df["Avg_Age"].round(1)

if display_df.empty:
    st.info("No clubs found matching your search.")
else:
    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
    )

# -----------------------------
# Export Data
# -----------------------------
st.divider()

st.subheader("📥 Export League Data")

csv = display_df.to_csv(index=False).encode("utf-8")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "📄 Download CSV",
        csv,
        file_name=f"{league}_clubs.csv",
        mime="text/csv",
        width="stretch",
    )

wb = Workbook()
ws = wb.active
ws.title = "League"

ws.append(display_df.columns.tolist())

for row in display_df.itertuples(index=False):
    ws.append(list(row))

excel_file = BytesIO()
wb.save(excel_file)
excel_file.seek(0)

with col2:
    st.download_button(
        "📊 Download Excel",
        excel_file,
        file_name=f"{league}_clubs.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch",
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
