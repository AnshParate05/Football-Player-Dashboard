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