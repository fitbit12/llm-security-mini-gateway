from typing import List, Tuple

from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_analyzer import PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# ---- Customization 1: Custom recognizer (API_KEY) ----
api_key_pattern = Pattern(
    name="api_key_pattern",
    regex=r"\bsk-[A-Za-z0-9]{8,}\b",
    score=0.85,
)

api_key_recognizer = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[api_key_pattern],
)

analyzer.registry.add_recognizer(api_key_recognizer)

def _context_boost(text: str, results: List[RecognizerResult]) -> List[RecognizerResult]:
    """
    ---- Customization 2: Context-aware scoring ----
    If sensitive words appear near an entity, increase its confidence a bit.
    """
    keywords = ["password", "otp", "secret", "token", "api key", "key"]
    t = text.lower()

    for r in results:
        window_start = max(0, r.start - 20)
        window_end = min(len(text), r.end + 20)
        window = t[window_start:window_end]

        if any(k in window for k in keywords):
            r.score = min(1.0, r.score + 0.10)

    return results
def _composite_risk(results: List[RecognizerResult]) -> bool:
    """
    ---- Customization 3: Composite detection ----
    If multiple high-risk entities appear together (e.g., email + phone),
    we treat the message as more sensitive.
    """
    types = {r.entity_type for r in results}
    return ("EMAIL_ADDRESS" in types and "PHONE_NUMBER" in types)


def analyze_and_mask(text: str, language: str = "en") -> Tuple[str, List[RecognizerResult], bool]:
    """
    Returns:
      masked_text: anonymized output
      results: list of detected entities
      composite_flag: True if composite risk triggered
    """
    results = analyzer.analyze(
        text=text,
        language=language,
        entities=["PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD", "API_KEY"],
    )

    results = _context_boost(text, results)
    composite_flag = _composite_risk(results)

    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized.text, results, composite_flag