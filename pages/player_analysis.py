import streamlit as st

from utils.data_loader import load_clean_data
from utils.styles import load_css

# ----------------------------------------------------
# Page Config
# ----------------------------------------------------

st.set_page_config(
    page_title="Player Analysis",
    page_icon="👤",
    layout="wide"
)

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

df = load_clean_data()

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.title("👤 Player Analysis")

player = st.sidebar.selectbox(
    "Select Player",
    sorted(df["Player"].unique())
)

# ----------------------------------------------------
# Filter Player
# ----------------------------------------------------

player_df = df[df["Player"] == player]

player_info = player_df.iloc[0]

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.title("👤 Player Analysis")

st.caption(
    "Explore detailed statistics for every player."
)

st.divider()

# ----------------------------------------------------
# Player Profile
# ----------------------------------------------------

st.subheader("📋 Player Profile")

col1, col2 = st.columns([1, 2])

with col1:

    st.markdown(
        f"""
        <div class="metric-card">

        <h2 style="margin-bottom:5px;">
        👤 {player_info['Player']}
        </h2>

        <p><b>Club</b><br>{player_info['Squad']}</p>

        <p><b>League</b><br>{player_info['Comp']}</p>

        <p><b>Position</b><br>{player_info['Pos']}</p>

        <p><b>Age</b><br>{player_info['Age']}</p>

        <p><b>Nationality</b><br>{player_info['Nation']}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.info(
        "Select another player from the sidebar to instantly update the profile and statistics."
    )

# ----------------------------------------------------
# Player Performance
# ----------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📊 Season Performance")

col1, col2, col3, col4 = st.columns(4)

cards = [
    ("⚽", "Goals", int(player_info["Gls"]), "#3B82F6"),
    ("🎯", "Assists", int(player_info["Ast"]), "#10B981"),
    ("⏱", "Minutes", int(player_info["Min"]), "#8B5CF6"),
    ("🟨", "Yellow Cards", int(player_info["CrdY"]), "#F59E0B"),
]

for column, (icon, title, value, color) in zip(
    [col1, col2, col3, col4],
    cards
):

    with column:

        st.markdown(
            f"""
<div class="metric-card" style="border-top:5px solid {color};">

<div class="metric-title">
{icon} {title}
</div>

<div class="metric-value">
{value}
</div>

</div>
""",
            unsafe_allow_html=True
        )

# ----------------------------------------------------
# Detailed Statistics
# ----------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📋 Detailed Statistics")

left, right = st.columns([2, 1])

with left:

    stats = {
        "Statistic": [
            "Goals",
            "Assists",
            "Minutes Played",
            "Yellow Cards",
            "Red Cards",
            "Age",
            "Position",
            "Club",
            "League"
        ],
        "Value": [
            int(player_info["Gls"]),
            int(player_info["Ast"]),
            int(player_info["Min"]),
            int(player_info["CrdY"]),
            int(player_info["CrdR"]),
            int(player_info["Age"]),
            player_info["Pos"],
            player_info["Squad"],
            player_info["Comp"]
        ]
    }

    st.table(stats)

with right:

    st.subheader("⏱ Minutes Played")

    minutes = int(player_info["Min"])

    max_minutes = 3420

    st.metric(
        "Minutes",
        f"{minutes:,}"
    )

    st.progress(
        min(minutes / max_minutes, 1.0)
    )

    st.caption(
        f"{minutes:,} / {max_minutes:,} possible minutes"
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