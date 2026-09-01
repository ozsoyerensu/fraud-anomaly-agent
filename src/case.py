from dataclasses import dataclass

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from features import add_features, FEATURES

@dataclass 
class Case:
    """A single flagged transaction, packaged for investigation."""

    transaction_id: int
    step: int
    type: str
    amount: float 

    sender_id: str
    sender_old_balance: float
    sender_new_balance: float

    receiver_id: str
    receiver_old_balance: float
    receiver_new_balance: float

    error_balance_orig: float
    error_balance_dest: float

    anomaly_score: float

    # Ground truth, for OUR evaluation only - the agent must NEVER see this.
    actual_is_fraud: bool 

    def to_agent_context(self) -> dict:
        """Exactly what the agent is allowed to see. actual_is_fraud is deliberately excluded- 
        \nshowing the agent the answer key would defeat the entire point of having it investiage."""
        return {
            "transaction_id": self.transaction_id, 
            "step": self.step,
            "type": self.type,
            "amount": self.amount, 
            "sender_id": self.sender_id, 
            "sender_old_balance": self.sender_old_balance,
            "sender_new_balance": self.sender_new_balance,
            "receiver_id": self.receiver_id,
            "receiver_old_balance": self.receiver_old_balance,
            "receiver_new_balance": self.receiver_new_balance,
            "error_balance_orig": self.error_balance_orig,
            "error_balance_dest": self.error_balance_dest,
            "anomaly_score": self.anomaly_score
        }

def load_scored_test_set():
    """Rebuild the exact same test from Module 3, then score with our saved model."""
    df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")
    df = add_features(df)
    df = df[df["type"].isin(["TRANSFER", "CASH_OUT"])].reset_index(drop=True)

    X = df[FEATURES]
    y = df["isFraud"]

    _, X_test, _, _ = train_test_split(X, y, test_size = 0.2, random_state=42, stratify = y)

    model = joblib.load("models/isolation_forest.joblib")
    anomaly_score = -model.score_samples(X_test)

    test_df = df.loc[X_test.index].copy()
    test_df["anomaly_score"] = anomaly_score
    return test_df 

def build_cases(test_df: pd.DataFrame, top_n: int = 10) -> list[Case]:
    """Turn the top_n most anomalous rows into Case objects."""
    top = test_df.nlargest(top_n, "anomaly_score") 

    cases = []
    for idx, row in top.iterrows():
        cases.append(Case(
            transaction_id = int(idx),
            step = int(row["step"]),
            type = row["type"],
            amount = float(row["amount"]),

            sender_id = row["nameOrig"],
            sender_old_balance = float(row["oldbalanceOrg"]),
            sender_new_balance = float(row["newbalanceOrig"]),

            receiver_id = row["nameDest"],
            receiver_old_balance = float(row["oldbalanceDest"]),
            receiver_new_balance = float(row["newbalanceDest"]),

            error_balance_orig = float(row["errorBalanceOrig"]),
            error_balance_dest = float(row["errorBalanceDest"]),

            anomaly_score = float(row["anomaly_score"]),

            actual_is_fraud = bool(row["isFraud"])
        ))
    return cases 

if __name__ == "__main__":
    test_df = load_scored_test_set()
    cases = build_cases(test_df, top_n=10)

    print(f"Build {len(cases)} cases from the top 10 most anomalous transactions.\n")
    for case in cases:
        print(f"Case #{case.transaction_id} - anomaly score: {case.anomaly_score:.3f}")
        print(" What the agent will see:", case.to_agent_context())
        print(f" (Actually fraud? {case.actual_is_fraud} - hidden from the agent)\n")



