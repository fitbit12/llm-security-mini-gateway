#policy_engine.py
from typing import List
from presidio_analyzer import RecognizerResult

from config import INJECTION_WARN_THRESHOLD, INJECTION_BLOCK_THRESHOLD

def decide_policy(inj_score: int, pii_results: List[RecognizerResult], composite_flag: bool) -> str:
    """
    Policy rules (simple & explainable):
    - Strong injection => BLOCK
    - Any PII => MASK
    - Composite PII => MASK (still) but can be noted as "high risk"
    - Otherwise => ALLOW
    """
    if inj_score >= INJECTION_BLOCK_THRESHOLD:
        return "BLOCK"

    if len(pii_results) > 0:
        return "MASK"

    if composite_flag:
        return "MASK"

    if inj_score >= INJECTION_WARN_THRESHOLD:
        return "ALLOW"  # allow but you can log warning

    return "ALLOW"