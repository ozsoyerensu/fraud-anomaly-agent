import json
import os

from dotenv import load_dotenv
from groq import Groq, BadRequestError

from case import Case, load_scored_test_set, build_cases
from tools import TOOLS, get_account_activity

load_dotenv()  # load environment variables from .env file

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"  # the model we will use for investigation

SYSTEM_PROMPT = """You are a fraud investigation analyst at a bank. You will be given details of a single flagged transaction that an automated anomaly-detection system has identified as potentially fraudulent.
Your job is to assess how suspicious the transaction is, and to provide a detailed explanation of your reasoning. Only call get_account_activity when you need account history — never call any other tool. When you are ready to give your final verdict, write the JSON object directly as your plain text response. Do not attempt to call a tool to produce your answer.

Respond with a JSON object with exactly the following fields:
- "risk_level": one of "low", "medium", or "high"
- "recommended_action": one of "clear", "hold_for_review", or "escalate"
- "explanation": a short (2-4 sentence) explanation of your reasoning, written in plain English. Avoid technical jargon.

Base your reasoning only on the transaction details provided. Do not assume information you were not given."""

AVAILABLE_TOOLS = {"get_account_activity": get_account_activity}
MAX_TOOLS_PER_INVESTIGATION = 5  # limit the number of tools the agent can call per investigation


def _recover_from_fake_tool_call(error: BadRequestError):
    """
    Groq sometimes has the model hallucinate a call to a nonexistent tool ("json" or "JSON") instead of
    returning its final answer as plain text. The API rejects the tool call with a 400 error - but the error
    body's 'failed_generation' field still contains the model's intended answer, embedded as the fake tool
    call's arguments. Rather than treating this as a hard failure, extract the answer directly.

    Returns the recovered verdict dict, or None if this wasn't that specific quirk (caller should treat it
    as a real error).
    """
    body = getattr(error, "body", None) or {}
    failed_generation = body.get("error", {}).get("failed_generation")
    if not failed_generation:
        return None

    try:
        parsed = json.loads(failed_generation)
        arguments = parsed.get("arguments")
        if isinstance(arguments, str):
            arguments = json.loads(arguments)
        if isinstance(arguments, dict) and "risk_level" in arguments:
            return arguments
    except (json.JSONDecodeError, AttributeError, TypeError):
        pass

    return None


def invetigate(case: Case) -> dict:
    """Send a case to the agent, letting it call tools before returning a verdict."""

    context = case.to_agent_context()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(context, indent=2)},
    ]

    for _ in range(MAX_TOOLS_PER_INVESTIGATION):
        try:
            response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=TOOLS,
                tool_choice="auto", temperature=0.2,
            )
        except BadRequestError as e:
            recovered = _recover_from_fake_tool_call(e)
            if recovered is not None:
                return recovered
            raise

        message = response.choices[0].message

        if not message.tool_calls:
            # No more tool calls, so the agent has finished its investigation.
            return json.loads(message.content)

        # The agent wants to use a tool. Record its request, then actually run it.
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in message.tool_calls
            ],
        })

        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            print(f" [agent is calling {func_name}({func_args})]")

            result = AVAILABLE_TOOLS[func_name](**func_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })

    raise RuntimeError("Agent didn't reach a final answer within the tool-call limit")


if __name__ == "__main__":
    test_df = load_scored_test_set()
    cases = build_cases(test_df, top_n=3)

    for case in cases:
        try:
            verdict = invetigate(case)
        except Exception as e:
            print(f"Case #{case.transaction_id}: investigation failed — {e}\n")
            continue

        print(f"Case #{case.transaction_id} (anomaly score {case.anomaly_score:.3f})")
        print(f" Verdict: {verdict}")
        print(f" Actually fraud? {case.actual_is_fraud} (hidden from the agent)\n")