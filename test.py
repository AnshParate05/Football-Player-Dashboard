import pandas as pd

# Load dataset
df = pd.read_csv("data/players_data-2025_2026.csv")

print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())