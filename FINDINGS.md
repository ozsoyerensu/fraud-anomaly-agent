# Project Notes & Decisions
## (1-Sep-2026) Finding:'errorBalanceDest' confuses busy legit account with mule accounts. 
**Where this came from:** inspecting the top 10 highest-anomaly-score cases printed by 'src/case.py', which scores transactions using the Isolation Forest trained in 'src/detector.py', using features built by 'src/features.py'.

**What we saw:** Of the top 10 cases by anomaly score, 9 were false positives and 1 was real fraud (transaction #2636011). The 9 false positives all showed the receiver's balance moving substantially during transaction. (e.g. case #1826709:'33','747','786' to '63','578','786'). The one real fraud case showed the receiver's balance at '0.0' *before and after* a $10,000,000 transfer - no trace of the money ever arriving. 

**Why this happens:** 'errorBalanceDest' measures the *magnitude* of the mismatch between expected and actual destination balance. A busy, legitimate account receiving multiple transactions within the same simulated time-step (PaySim's 'step' field) produces a large mismatch too, purely as an artifact of aggregation - not bc anything is wrong. My feature cannot distinguish "busy legit account" from "suspicious mule account"; both look like a big number. 

**Decision:** Add a new, more targeted feature to 'src/features.py': 'destBalanceStayedZero' - flags whether the receiving account shows zero balance both before and after a transaction that moved real money. This targets the fraud-specific pattern directly, instead of relying on 'errorBalanceDest's magnitude alone. 

**Next step:** retrain ('src/detector.py'), rebuild cases ('src/case.py), and compare the new top 10 list against this one. 

**Results:** After adding 'destBalanceStayedZero', average precision rose from 0.0663 to 0.0990, and the real fraud case moved from rank #2 to rank #1 in the top 10 list by anomaly score. However, the other 9 top 10 cases are unchanged. They're still flagged due to 'errorBalanceDest's magnitude, driven by the same multi-transaction-per-step aggregation pattern, which a single-row feature can't distinguish from real fraud. Fixing that likely requires *account-level context* (e.g. how many transactions this receiver handled in this time-step) which points toward giving the agent a tool to look up account history, rather than trying to hand-craft a perfect feature. 
