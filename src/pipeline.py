import time
from datetime import datetime
from case import load_scored_test_set, build_cases
from agent import invetigate

TOP_N = 15  # Number of top anomalies to investigate. Small bc each case costs a real API call.


def run_pipeline(top_n: int = TOP_N):
    test_df = load_scored_test_set()
    cases = build_cases(test_df, top_n)

    results = []
    pipeline_start = time.perf_counter()

    for case in cases:
        print(f"Investigating case #: {case.transaction_id}")
        case_start = time.perf_counter()
        try:
            verdict = invetigate(case)
        except Exception as e:
            verdict = {
                "risk_level": "ERROR",
                "recommended_action": "N/A",
                "explanation": f"Investigation failed: {e}",
            }
        elapsed = time.perf_counter() - case_start
        results.append({"case": case, "verdict": verdict, "elapsed_seconds": elapsed})

    total_elapsed = time.perf_counter() - pipeline_start
    return results, total_elapsed


def write_report(results, total_elapsed, path="reports/investigation_report.md"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Fraud Investigation Report",
        f"Generated: {timestamp}",
        f"Cases reviewed: {len(results)}",
        "",
    ]

    flagged_high = 0
    caught_among_flagged = 0
    total_actual_fraud = 0

    for r in results:
        case = r["case"]
        verdict = r["verdict"]
        risk = str(verdict.get("risk_level", "UNKNOWN"))

        is_high = "HIGH" in risk.upper()
        if is_high:
            flagged_high += 1
            if case.actual_is_fraud:
                caught_among_flagged += 1
        if case.actual_is_fraud:
            total_actual_fraud += 1

        lines.append(f"## Case #{case.transaction_id}")
        lines.append(f"- Amount: {case.amount:.2f}")
        lines.append(f"- Anomaly score: {case.anomaly_score:.3f}")
        lines.append(f"- Investigation time: {r['elapsed_seconds']:.2f}s")
        lines.append(f"- Agent risk level: {risk}")
        lines.append(f"- Recommended action: {verdict.get('recommended_action', 'N/A')}")
        lines.append(f"- Explanation: {verdict.get('explanation', 'N/A')}")
        lines.append(f"- Actually fraud (ground truth, hidden from the agent): {bool(case.actual_is_fraud)}")
        lines.append("")

    lines.append("## Summary")
    lines.append(f"- Total cases reviewed: {len(results)}")
    lines.append(f"- Flagged HIGH risk by agent: {flagged_high}")
    lines.append(f"- Of those, actually fraud: {caught_among_flagged}")
    lines.append(f"- Total actual fraud among reviewed cases: {total_actual_fraud}")
    avg_time = total_elapsed / len(results) if results else 0
    lines.append(f"- Total pipeline time: {total_elapsed:.2f}s")
    lines.append(f"- Average time per case: {avg_time:.2f}s")
    if flagged_high > 0:
        precision = caught_among_flagged / flagged_high
        lines.append(f"- Precision at HIGH-risk flags: {precision:.2%}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nReport written to {path}")


if __name__ == "__main__":
    results, total_elapsed = run_pipeline()
    write_report(results, total_elapsed)