import pandas as pd


def load_clean_data():
    """
    Load the cleaned football dataset.
    """

    df = pd.read_csv("data/cleaned_players.csv")

    return df