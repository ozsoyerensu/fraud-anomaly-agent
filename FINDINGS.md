# Project Notes & Decisions
## (1-Sep-2026) Finding:'errorBalanceDest' confuses busy legit account with mule accounts. 
**Where this came from:** inspecting the top 10 highest-anomaly-score cases printed by 'src/case.py', which scores transactions using the Isolation Forest trained in 'src/detector.py', using features built by 'src/features.py'.

**What we saw:** Of the top 10 cases by anomaly score, 9 were false positives and 1 was real fraud (transaction #2636011). The 9 false positives all showed the receiver's balance moving substantially during transaction. (e.g. case #1826709:'33','747','786' to '63','578','786'). The one real fraud case showed the receiver's balance at '0.0' *before and after* a $10,000,000 transfer - no trace of the money ever arriving. 

**Why this happens:** 'errorBalanceDest' measures the *magnitude* of the mismatch between expected and actual destination balance. A busy, legitimate account receiving multiple transactions within the same simulated time-step (PaySim's 'step' field) produces a large mismatch too, purely as an artifact of aggregation - not bc anything is wrong. My feature cannot distinguish "busy legit account" from "suspicious mule account"; both look like a big number. 

**Decision:** Add a new, more targeted feature to 'src/features.py': 'destBalanceStayedZero' - flags whether the receiving account shows zero balance both before and after a transaction that moved real money. This targets the fraud-specific pattern directly, instead of relying on 'errorBalanceDest's magnitude alone. 

**Next step:** retrain ('src/detector.py'), rebuild cases ('src/case.py), and compare the new top 10 list against this one. 

**Results:** After adding 'destBalanceStayedZero', average precision rose from 0.0663 to 0.0990, and the real fraud case moved from rank #2 to rank #1 in the top 10 list by anomaly score. However, the other 9 top 10 cases are unchanged. They're still flagged due to 'errorBalanceDest's magnitude, driven by the same multi-transaction-per-step aggregation pattern, which a single-row feature can't distinguish from real fraud. Fixing that likely requires *account-level context* (e.g. how many transactions this receiver handled in this time-step) which points toward giving the agent a tool to look up account history, rather than trying to hand-craft a perfect feature. 

**Update:** the agent, working from a single transaction's data alone, made the exact same false-positive calls on these same two accounts as the raw anomaly score did, for the same underlying reason (no account-history context). I will give an agent a tool to look up an account's recent activity should let it distinguish a busy legitimate account from a genuine one-off drain, instead of re-deriving the ML model's blind spot. 

## Model quirk: occasional invalid "json" tool call

**Where:** `src/agent.py`, `invetigate()` — surfaced during Module 6 tool-calling testing.

**What we saw:** After using `get_account_activity`, the model (`openai/gpt-oss-120b`
via Groq) occasionally tries to finish by calling a nonexistent tool named `json`
instead of writing its JSON verdict as plain text — even after the system prompt was
updated to explicitly forbid this. Groq's API correctly rejects the malformed request.

**Why we're not chasing a perfect prompt fix:** this is a known characteristic of
smaller/open-weight models blending "produce structured output" with "call a function"
when both are active at once. Prompting reduced the frequency but didn't eliminate it.

**Mitigation:** `invetigate()` calls are wrapped in a try/except in the batch loop, so
one case failing this way is logged and skipped rather than crashing the whole run —
the resilience a real system needs regardless of which specific quirk causes a failure.

**Possible future improvement:** an automatic one-time retry when this specific error
is detected — `failed_generation` in the error response usually contains the model's
actual intended answer, just packaged wrong, so a retry would likely succeed.