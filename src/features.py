import pandas as pd

FEATURES = ["amount", "oldbalanceOrg", "errorBalanceOrig", "errorBalanceDest", "destBalanceStayedZero"]


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add engineered columns that help spot suspicious transactions."""
    df = df.copy()

    df["errorBalanceOrig"] = df["oldbalanceOrg"] - df["amount"] - df["newbalanceOrig"]
    df["errorBalanceDest"] = df["oldbalanceDest"] + df["amount"] - df["newbalanceDest"]

    # Does the receiving account show zero activity despite money moving through it?
    # A busy legit account's balance actually changes; a mule account often shows nothing.
    df["destBalanceStayedZero"] = (
        (df["oldbalanceDest"] == 0) & (df["newbalanceDest"] == 0) & (df["amount"] > 0)
    ).astype(int)

    return df


if __name__ == "__main__":
    df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")
    df = add_features(df)

    print("Balance error stats for LEGIT transactions:")
    print(df[df["isFraud"] == 0][["errorBalanceOrig", "errorBalanceDest"]].describe())

    print("\nBalance error stats for FRAUD transactions:")
    print(df[df["isFraud"] == 1][["errorBalanceOrig", "errorBalanceDest"]].describe())

    print("\nShare of transactions where the destination balance stayed at exactly zero:")
    print(df.groupby("isFraud")["destBalanceStayedZero"].mean())