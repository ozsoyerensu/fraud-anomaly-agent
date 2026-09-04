# Fraud Investigation Report
Generated: 2026-09-04 14:20:10
Cases reviewed: 15

## Case #2736011
- Amount: 10000000.00
- Anomaly score: 0.856
- Investigation time: 14.83s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The transfer is for a huge amount (10 million) from an account that has only ever been involved in a single transaction, and the balances for both parties did not change, indicating a likely error or fraud. Combined with a high anomaly score, this warrants immediate escalation.
- Actually fraud (ground truth, hidden from the agent): True

## Case #1994274
- Amount: 10000000.00
- Anomaly score: 0.849
- Investigation time: 5.59s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender has only ever made one transaction and emptied an account that did not have sufficient funds, while the receiver is a frequent large-sum recipient. The huge amount, negative balance errors, and high anomaly score all point to a likely fraudulent transfer.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1844068
- Amount: 10000000.00
- Anomaly score: 0.844
- Investigation time: 5.33s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender has only ever made this single transaction, draining their entire balance and sending far more than they possessed, which is a clear red flag. The receiver has repeatedly been on the receiving end of large sums, suggesting a possible funnel for illicit funds.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1829165
- Amount: 10000000.00
- Anomaly score: 0.843
- Investigation time: 4.71s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender, with only a single prior transaction, emptied their account by sending far more than their balance, creating large negative balance errors. The receiver is a frequent sink for large sums, and the transaction amount and anomaly score are unusually high, indicating likely fraud.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1826709
- Amount: 12012625.01
- Anomaly score: 0.843
- Investigation time: 6.46s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender has only one prior transaction and is trying to send far more than their available balance, causing negative balance errors. The receiver is a frequent recipient of large sums, and the transaction amount and balance mismatches are extreme, indicating a likely fraudulent transfer.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1839508
- Amount: 10000000.00
- Anomaly score: 0.842
- Investigation time: 4.19s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender attempted to transfer 10 million dollars despite only having about half a million, resulting in a negative balance error. This is the sender's only transaction ever, while the receiver has repeatedly received large sums, suggesting a possible money‑mule scheme. The high anomaly score and impossible fund source make this transaction highly suspicious.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1832886
- Amount: 10000000.00
- Anomaly score: 0.842
- Investigation time: 12.20s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender account has only ever made a single transaction and emptied its balance, sending far more than it possessed, while the receiver is a frequent recipient with a large cumulative inflow. The large amount, balance mismatches, and high anomaly score together indicate a strong likelihood of fraud.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1824010
- Amount: 10000000.00
- Anomaly score: 0.842
- Investigation time: 11.22s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender account has only ever made a single transaction and sent an amount far exceeding its balance, leaving it at zero and creating a large negative error balance. The receiver has repeatedly received large sums, suggesting a possible money‑mule pattern, and the high anomaly score confirms the suspicion.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1827031
- Amount: 10000000.00
- Anomaly score: 0.842
- Investigation time: 17.23s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender account has only ever been used once and is trying to send $10 million, far exceeding its $440k balance, creating a negative balance error. The receiver has repeatedly received large sums and this transfer inflates its balance by over $30 million, matching a high anomaly score. These factors together indicate a very suspicious transaction.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1828534
- Amount: 10000000.00
- Anomaly score: 0.842
- Investigation time: 13.17s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender account has only ever been used once and sent an amount far exceeding its balance, creating a large negative error balance. The receiver has repeatedly received large sums, suggesting a possible money‑mule pattern, and the transaction’s high anomaly score confirms the suspicion.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1824374
- Amount: 10000000.00
- Anomaly score: 0.842
- Investigation time: 12.64s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender, with only one prior transaction, attempted to transfer far more than their available balance, leaving a zero balance and generating large error amounts. The receiver's balance jumps to over 24 million, and the anomaly score is very high, indicating a likely fraudulent scheme.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1829756
- Amount: 10000000.00
- Anomaly score: 0.841
- Investigation time: 16.89s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender attempted to transfer far more than their available balance, resulting in negative error balances, and this is their only transaction ever. The receiver has repeatedly received large sums, acting like a cash‑collector account. Combined with a high anomaly score, this pattern strongly suggests fraudulent activity.
- Actually fraud (ground truth, hidden from the agent): False

## Case #2008442
- Amount: 10000000.00
- Anomaly score: 0.841
- Investigation time: 4.30s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender attempted to transfer ten million dollars despite only having about $630k in the account, resulting in a negative balance error. The receiver's balance jumps from zero to over $16 million, and the anomaly score is very high, indicating a likely fraudulent transaction.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1826076
- Amount: 10000000.00
- Anomaly score: 0.841
- Investigation time: 13.49s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The sender has only ever made one transaction and is trying to transfer far more than their available balance, causing large balance errors. The receiver has repeatedly received large sums, suggesting a possible collection account. Combined with a high anomaly score, this pattern is highly suspicious.
- Actually fraud (ground truth, hidden from the agent): False

## Case #1809334
- Amount: 31957701.91
- Anomaly score: 0.840
- Investigation time: 9.24s
- Agent risk level: high
- Recommended action: escalate
- Explanation: The transfer moves about $32 million from an account that previously held only $74 k, leaving it with a zero balance and a large negative error balance, which is impossible under normal operations. The receiver's balance more than doubles, and the anomaly score is very high, indicating a likely fraudulent activity.
- Actually fraud (ground truth, hidden from the agent): False

## Summary
- Total cases reviewed: 15
- Flagged HIGH risk by agent: 15
- Of those, actually fraud: 1
- Total actual fraud among reviewed cases: 1
- Total pipeline time: 151.50s
- Average time per case: 10.10s
- Precision at HIGH-risk flags: 6.67%