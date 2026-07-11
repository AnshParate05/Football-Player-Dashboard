from utils.preprocessing import load_data, clean_data

df = load_data()

clean_df = clean_data(df)

clean_df.to_csv("data/cleaned_players.csv", index=False)

print("Dataset cleaned successfully!")
print(clean_df.head())
print(clean_df.shape)