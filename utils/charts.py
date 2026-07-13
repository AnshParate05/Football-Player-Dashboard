import plotly.express as px


def league_chart(df):

    league = df["Comp"].value_counts().reset_index()

    league.columns = ["League","Players"]

    fig = px.bar(
        league,
        x="League",
        y="Players",
        color="Players",
        title="Players in Each League"
    )

    return fig

def position_chart(df):

    # Split positions like "MF,FW"
    positions = (
        df["Pos"]
        .fillna("")
        .str.split(",")
        .explode()
        .str.strip()
    )

    mapping = {
        "GK": "Goalkeeper",
        "DF": "Defender",
        "MF": "Midfielder",
        "FW": "Forward"
    }

    positions = positions.replace(mapping)

    position_df = (
        positions.value_counts()
        .reset_index()
    )

    position_df.columns = ["Position", "Players"]

    fig = px.pie(
        position_df,
        names="Position",
        values="Players",
        hole=0.55,
        title="Player Position Distribution",
        color_discrete_sequence=[
            "#3B82F6",
            "#10B981",
            "#F59E0B",
            "#8B5CF6"
        ]
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        pull=[0.03, 0, 0, 0]
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title="Position"
    )

    return fig