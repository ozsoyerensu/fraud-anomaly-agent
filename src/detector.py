import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix

from features import add_features

FEATURES = ["amount", "oldbalanceOrg", "errorBalanceOrig", "errorBalanceDest"]

def load_risky_transactions():
    df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")
    df = add_features(df)
    return df[df["type"].isin(["TRANSFER", "CASH_OUT"])].reset_index(drop=True)

if __name__ == "__main__":
    df = load_risky_transactions()

    X = df[FEATURES]
    y = df["isFraud"] 

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify = y)

    fraud_rate = y_train.mean()
    print(f"Training on {len(X_train):,} transactions, fraud rate: {fraud_rate: .4%}")

    model = IsolationForest(
        n_estimators=200,
        contamination= fraud_rate,
        random_state=42, 
        n_jobs = -1,
    )

model.fit(X_train) # note: y_train is never passed in here. The model never sees labels. 

raw_preds = model.predict(X_test) #sklearn returns 1 for normal, -1 for anomaly. We want 0 for normal, 1 for anomaly.
y_pred = (raw_preds == -1).astype(int) #convert to 1 for flagged, 0 for not flagged. 

print("\nConfusion matrix (rows = actual, columns = predicted):")
print(confusion_matrix(y_test, y_pred))

print("\nClassification report:")
print(classification_report(y_test, y_pred, digits=4))

from sklearn.metrics import precision_recall_curve, average_precision_score

# score samples: higher = more "normal". We flip the sign so that higher = more suspicious.
anomaly_score = -model.score_samples(X_test)

ap = average_precision_score(y_test, anomaly_score)
print(f"\nAverage precision (area under the precision-recall curve): {ap:.4f}")

# instead of a fixed yes/no cutoff, flag the top 1% most suspicious transactions.
cutoff= pd.Series(anomaly_score).quantile(0.99)
flagged = (anomaly_score >= cutoff).astype(int)

print(f"\nFlagging the top 1% most suspicious transactions: {flagged.sum()} of them):")
print(classification_report(y_test, flagged, digits=3))

joblib.dump(model, "models/isolation_forest.joblib")
print("\nSaved model to models/isolation_forest.joblib")
