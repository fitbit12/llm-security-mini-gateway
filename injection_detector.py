# injection_detector.py

SUSPICIOUS_PHRASES = [
    "ignore previous instructions",
    "reveal the system prompt",
    "show me your hidden instructions",
    "bypass safety",
    "jailbreak",
    "act as developer mode",
]

def injection_score(text: str) -> int:
    """
    Returns an integer score.
    Higher score means higher likelihood of injection/jailbreak attempt.
    """
    t = text.lower()
    score = 0

    for phrase in SUSPICIOUS_PHRASES:
        if phrase in t:
            score += 1

    return score