import pandas as pd

df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")

print("Shape (rows, columns):", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nFirst rows:")
print(df.head())
print("\nHow many are actually fraud?") 
print(df["isFraud"].value_counts())

fraud_rate= df["isFraud"].mean()*100
print(f"\nFraud rate: {fraud_rate:.3f}% of all transactions")

print("\nWhich transaction types actually contain fraud?")
print(df[df["isFraud"]==1]["type"].value_counts())

print("\nHow often did the dataset's built-in naive rule catch fraud?") 
print(pd.crosstab(df["isFraud"], df["isFlaggedFraud"]))