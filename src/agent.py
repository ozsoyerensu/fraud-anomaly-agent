import json 
import os

from dotenv import load_dotenv
from groq import Groq 

from case import Case, load_scored_test_set, build_cases

load_dotenv() # load environment variables from .env file

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b" # the model we will use for investigation

SYSTEM_PROMPT = """You are a fraud investigation analyst at a bank. You will be given details of a single " \
"\nflagged transaction that an automated anomaly-detection system has identified as potentially fraudulent.\
\nYour job is to assess how suspicious the transaction is, and to provide a detailed explanation of your reasoning."

Respond with a JSON object with exactly the following fields:
-"risk_level": one of "low", "medium", or "high"
-"recommended_action": one of "clear", "hold_for_review", or "escalate"
-"explanation": a short (2-4 sentence) explanation of your reasoning, written in plain English. Avoid technical jargon.

Base your reasoning only on the reasoning only on the transaction details provided. Do not assume information \ 
\nyou were not given."""

def invetigate(case:Case) -> dict:
    """Send a single flagged transaction to the agent for investigation, and return its response as a dict."""

    context = case.to_agent_context()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(context, indent=2)},
        ],
        response_format={"type":"json_object"},
        temperature=0.2,
    )

    return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
    test_df = load_scored_test_set()
    cases = build_cases(test_df, top_n=3)

    for case in cases:
        verdict = invetigate(case)
        print(f"Case #{case.transaction_id} (anomaly score {case.anomaly_score:.3f})")
        print(f" Verdict: {verdict}")
        print(f" Actually fraud? {case.actual_is_fraud} (hidden from the agent)\n")
