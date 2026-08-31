import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame: 
    """Add engineered columns that help spot suspicious activities.""" 
    df = df.copy()

    # Does the sender's balance math actually add up?
    # Legit transactions: oldbalanceOrg - amount = newbalanceOrig
    df['errorBalanceOrig'] = df['oldbalanceOrg'] - df['amount'] - df['newbalanceOrig']

    # Same check for the receiver's balance
    df['errorBalanceDest'] = df['oldbalanceDest'] + df[ 'amount'] - df['newbalanceDest'] 

    return df

if __name__ == "__main__":
    df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")
    df = add_features(df)

    # Compare apples to apples: fraud only happens in these two transaction types
    risky = df[df["type"].isin(["TRANSFER", "CASH_OUT"])]

    print("Balance error stats for LEGIT TRANSFER/CASH OUT transactions:")
    print(risky[risky['isFraud'] == 0][["errorBalanceOrig", "errorBalanceDest"]].describe())

    print("\nBalance error stats for FRAUD transactions:")
    print(risky[risky['isFraud'] == 1][["errorBalanceOrig", "errorBalanceDest"]].describe())