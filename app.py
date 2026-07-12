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

metrics = dashboard_metrics(df)

st.title("⚽ Football Analytics Dashboard")

st.caption("Top 5 European Leagues 2025-26")

# ---------------- KPI ----------------

col1,col2,col3,col4 = st.columns(4)

col1.metric("Players",metrics["players"])
col2.metric("Clubs",metrics["clubs"])
col3.metric("Leagues",metrics["leagues"])
col4.metric("Goals",metrics["goals"])

# ---------------- Chart ----------------

fig = league_chart(df)

st.plotly_chart(fig,use_container_width=True)