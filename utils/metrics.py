def dashboard_metrics(df):

    return {
        "players": df["Player"].nunique(),
        "clubs": df["Squad"].nunique(),
        "leagues": df["Comp"].nunique(),
        "goals": int(df["Gls"].sum())
    }