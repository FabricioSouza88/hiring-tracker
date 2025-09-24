from __future__ import annotations
import re
from typing import List, Tuple

def parse_score_and_decision(text: str) -> Tuple[float | None, str | None, List[str]]:
    """
    Looks for patterns like:
      Score: 7.5/10
      Decision: approved | hold | rejected
      feedback: ...
      Labels: python, agents, azure
    Returns (score, decision, labels)
    """
    score = None
    decision = None
    feedback = None
    labels: List[str] = []

    # Score
    m = re.search(r"Score:\s*([0-9]+(?:\.[0-9]+)?)\s*/\s*10", text, re.IGNORECASE)
    if m:
        try:
            score = float(m.group(1))
        except ValueError:
            score = None

    # Decision
    m = re.search(r"Decision:\s*(approved|hold|rejected)", text, re.IGNORECASE)
    if m:
        decision = m.group(1).lower()

    # Rationale / Feedback
    m = re.search(r"Rationale:\s*(.+?)(?=\n\s*(?:Score|Decision|Labels)|\Z)", text, re.IGNORECASE | re.DOTALL)
    if m:
        feedback = m.group(1).strip()

    # Labels (comma or semicolon separated)
    m = re.search(r"Labels?:\s*([a-z0-9_,;\-\s]+)$", text, re.IGNORECASE | re.MULTILINE)
    if m:
        raw = m.group(1)
        labels = [x.strip().lower() for x in re.split(r"[;,]", raw) if x.strip()]

    return score, decision, feedback, labels
