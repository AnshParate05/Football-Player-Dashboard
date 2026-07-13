def dashboard_metrics(df):

    return {
        "players": df["Player"].nunique(),
        "clubs": df["Squad"].nunique(),
        "leagues": df["Comp"].nunique(),
        "goals": int(df["Gls"].sum())
    }

def top_goal_scorers(df, limit=10):

    columns = ["Player", "Squad", "Gls", "Ast", "Min"]

    top_players = (
        df[columns]
        .sort_values(by="Gls", ascending=False)
        .head(limit)
        .reset_index(drop=True)
    )

    top_players.index += 1
    top_players.index.name = "Rank"

    return top_players