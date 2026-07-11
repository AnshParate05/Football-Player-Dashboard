import pandas as pd


def load_data():
    """Load the original dataset"""
    df = pd.read_csv("data/players_data-2025_2026.csv")
    return df


def clean_data(df):
    """Clean dataset and create new features"""

    columns = [
        "Player",
        "Nation",
        "Pos",
        "Squad",
        "Comp",
        "Age",
        "MP",
        "Starts",
        "Min",
        "90s",
        "Gls",
        "Ast",
        "G+A",
        "PK",
        "PKatt",
        "CrdY",
        "CrdR"
    ]

    df = df[columns].copy()

    df.drop_duplicates(inplace=True)

    # Fill missing values
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna("Unknown")

    # Prevent division by zero
    df["90s"] = df["90s"].replace(0, 1)
    df["MP"] = df["MP"].replace(0, 1)

    # ---------- Feature Engineering ----------

    df["Goals_per90"] = (df["Gls"] / df["90s"]).round(2)

    df["Assists_per90"] = (df["Ast"] / df["90s"]).round(2)

    df["Goal_Contribution"] = df["Gls"] + df["Ast"]

    df["Minutes_per_Match"] = (df["Min"] / df["MP"]).round(2)

    return df