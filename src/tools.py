import pandas as pd

from features import add_features

_full_df= None # cached so we don't have to reload the data every time

def _load_full_df():
    global _full_df 
    if _full_df is None:
        df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")
        _full_df = add_features(df)
    return _full_df

def get_account_activity(account_id:str) -> dict:
    """Look up how many transactions an account has been involved in, as sender or
    receiver, across the full transaction history. Does NOT reveal whether any of
    those transactions were fraud — just how active the account is."""
    df = _load_full_df()
    involved = df[(df["nameOrig"] == account_id) | (df["nameDest"] == account_id)]

    return {
        "account_id": account_id,
        "total_transactions": int(len(involved)),
        "times_as_sender": int((involved["nameOrig"] == account_id).sum()),
        "times_as_receiver": int((involved["nameDest"] == account_id).sum()),
        "total_amount_received": float(involved[involved["nameDest"] == account_id]["amount"].sum())
    }

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_account_activity",
            "description": (
                "Look up how many transactions an account (sender or receiver) has been "
                "involved in across the full transaction history. Use this to check whether "
                "an account is busy and frequently used (like a business or agent) versus "
                "one that rarely appears — which matters for telling apart a legitimate "
                "high-volume account from a suspicious one-off destination."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "The account ID to look up, e.g. 'C1234567890'.",
                    }
                },
                "required": ["account_id"]
            }

        }

    }
]


