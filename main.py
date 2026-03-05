# main.py

from config import DEFAULT_LANGUAGE
from injection_detector import injection_score
from presidio_engine import analyze_and_mask
from policy_engine import decide_policy
from latency import measure_ms

from scenarios import SCENARIOS


def run_one(text: str):
    (inj_score, inj_ms) = measure_ms(injection_score, text)

    ((masked_text, pii_results, composite_flag), pii_ms) = measure_ms(
        analyze_and_mask, text, DEFAULT_LANGUAGE
    )

    (decision, policy_ms) = measure_ms(
        decide_policy, inj_score, pii_results, composite_flag
    )

    return {
        "input": text,
        "injection_score": inj_score,
        "pii_count": len(pii_results),
        "pii_types": [r.entity_type for r in pii_results],
        "composite_flag": composite_flag,
        "decision": decision,
        "output": "[BLOCKED]" if decision == "BLOCK" else masked_text,
        "latency_ms": {
            "injection": round(inj_ms, 2),
            "presidio": round(pii_ms, 2),
            "policy": round(policy_ms, 2),
            "total": round(inj_ms + pii_ms + policy_ms, 2),
        },
    }


def main():
    print("=== LLM Security Mini-Gateway (Practice Build) ===\n")

    for s in SCENARIOS:
        print(f"--- Scenario: {s['name']} ---")
        result = run_one(s["text"])

        print("Decision:", result["decision"])
        print("Injection Score:", result["injection_score"])
        print("PII Types:", result["pii_types"])
        print("Output:", result["output"])
        print("Latency (ms):", result["latency_ms"])
        print()


if __name__ == "__main__":
    main()