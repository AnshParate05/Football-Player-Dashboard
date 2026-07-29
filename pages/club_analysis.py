import streamlit as st

from utils.data_loader import load_clean_data
from utils.styles import load_css
from io import BytesIO
from openpyxl import Workbook

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Club Analysis",
    page_icon="🏟",
    layout="wide"
)

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

df = load_clean_data()

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.title("🏟 Club Analysis")

club = st.sidebar.selectbox(
    "Select Club",
    sorted(df["Squad"].unique())
)

# ----------------------------------------------------
# Filter Club
# ----------------------------------------------------

club_df = df[df["Squad"] == club]

# ----------------------------------------------------
# Club Information
# ----------------------------------------------------

league = str(club_df["Comp"].iloc[0]).split(maxsplit=1)[-1]

players = club_df["Player"].nunique()

avg_age = round(club_df["Age"].mean(), 1)

goals = int(club_df["Gls"].sum())

assists = int(club_df["Ast"].sum())

minutes = int(club_df["Min"].sum())

# ----------------------------------------------------
# Page Header
# ----------------------------------------------------

st.title("🏟 Club Analysis")

st.caption(
    "Explore club performance, squad statistics and top-performing players."
)

st.divider()

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.markdown(
    f"""
<div class="club-banner">

<div class="club-banner-row">

<div>
<h1>{club}</h1>
</div>

<div>
<h3>{league}</h3>
</div>

</div>

</div>
""",
    unsafe_allow_html=True,
)

st.markdown("## 📊 Club Overview")

goal_per_player = round(goals / players, 2) if players else 0

cards = [
    ("⚽ Goals", goals),
    ("🎯 Assists", assists),
    ("👥 Players", players),
    ("📈 Goals / Player", goal_per_player),
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
st.markdown("<br><br>", unsafe_allow_html=True)

st.subheader("⚔️ Player Comparison")

compare_col1, compare_col2 = st.columns(2)

players_list = sorted(club_df["Player"].unique())

with compare_col1:
    player1 = st.selectbox(
        "Select Player 1",
        players_list,
        key="player1"
    )

with compare_col2:
    player2 = st.selectbox(
        "Select Player 2",
        players_list,
        index=1 if len(players_list) > 1 else 0,
        key="player2"
    )

p1 = club_df[club_df["Player"] == player1].iloc[0]
p2 = club_df[club_df["Player"] == player2].iloc[0]

comparison_df = {
    "Metric": [
        "Position",
        "Age",
        "Goals",
        "Assists",
        "Minutes",
    ],
    player1: [
        p1["Pos"],
        p1["Age"],
        p1["Gls"],
        p1["Ast"],
        f'{int(p1["Min"]):,}',
    ],
    player2: [
        p2["Pos"],
        p2["Age"],
        p2["Gls"],
        p2["Ast"],
        f'{int(p2["Min"]):,}',
    ]
}

st.table(comparison_df)

st.divider()

st.markdown("## 📊 Team Leaders")

chart1, chart2 = st.columns(2)

with chart1:

    st.markdown("### ⚽ Top Goal Scorers")

    top_goals = club_df.sort_values(
        "Gls",
        ascending=False
    ).head(10)

    st.bar_chart(
        top_goals.set_index("Player")["Gls"]
    )

with chart2:

    st.markdown("### 🎯 Top Assist Providers")

    top_ast = club_df.sort_values(
        "Ast",
        ascending=False
    ).head(10)

    st.bar_chart(
        top_ast.set_index("Player")["Ast"]
    )

st.markdown("## 👥 Squad Overview")

search = st.text_input(
    "🔍 Search Player"
)

table = club_df.copy()

if search:

    table = table[
        table["Player"].str.contains(
            search,
            case=False
        )
    ]

st.dataframe(

    table[
        [
            "Player",
            "Pos",
            "Age",
            "Gls",
            "Ast",
            "Min"
        ]
    ],

    use_container_width=True,
    hide_index=True

)

st.divider()

st.subheader("📥 Export Squad Data")

export_df = club_df[
    [
        "Player",
        "Pos",
        "Age",
        "Gls",
        "Ast",
        "Min"
    ]
].copy()

csv = export_df.to_csv(index=False).encode("utf-8")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name=f"{club}_squad.csv",
        mime="text/csv",
        use_container_width=True
    )

wb = Workbook()
ws = wb.active
ws.title = "Squad"

ws.append(export_df.columns.tolist())

for row in export_df.itertuples(index=False):
    ws.append(list(row))

excel_file = BytesIO()
wb.save(excel_file)
excel_file.seek(0)

with col2:
    st.download_button(
        label="📊 Download Excel",
        data=excel_file,
        file_name=f"{club}_squad.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
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
