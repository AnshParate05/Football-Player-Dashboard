# ==========================================================
# Dashboard Metrics
# ==========================================================

def dashboard_metrics(df):
    """
    Returns the main dashboard KPI metrics.
    """

    return {
        "players": df["Player"].nunique(),
        "clubs": df["Squad"].nunique(),
        "leagues": df["Comp"].nunique(),
        "goals": int(df["Gls"].sum())
    }


# ==========================================================
# Top Goal Scorers
# ==========================================================

def top_goal_scorers(df, limit=10):
    """
    Returns the top goal scorers.
    """

    columns = [
        "Player",
        "Squad",
        "Gls",
        "Ast",
        "Min"
    ]

    top_players = (
        df[columns]
        .sort_values(
            by="Gls",
            ascending=False
        )
        .head(limit)
        .reset_index(drop=True)
    )

    top_players.index += 1
    top_players.index.name = "Rank"

    return top_players


# ==========================================================
# Top Assist Providers
# ==========================================================

def top_assist_providers(df, limit=10):
    """
    Returns the top assist providers.
    """

    columns = [
        "Player",
        "Squad",
        "Ast",
        "Gls",
        "Min"
    ]

    top_players = (
        df[columns]
        .sort_values(
            by="Ast",
            ascending=False
        )
        .head(limit)
        .reset_index(drop=True)
    )

    top_players.index += 1
    top_players.index.name = "Rank"

    return top_players


# ==========================================================
# Featured Statistics
# (Useful for Player Analysis Page)
# ==========================================================

def average_age(df):
    """
    Returns average player age.
    """

    if df.empty:
        return 0

    return round(df["Age"].mean(), 1)


def total_minutes(df):
    """
    Returns total minutes played.
    """

    return int(df["Min"].sum())


def total_assists(df):
    """
    Returns total assists.
    """
    return int(df["Ast"].sum())


def total_red_cards(df):
    """
    Returns total red cards.
    """

    return int(df["CrdR"].sum())


def total_yellow_cards(df):
    """
    Returns total yellow cards.
    """

    return int(df["CrdY"].sum())
