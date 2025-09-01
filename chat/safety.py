import re

EMERGENCY_PATTERNS = [
    r"chest pain", r"severe bleeding", r"trouble breathing", r"stroke", r"unconscious",
    r"overdose", r"suicidal", r"fracture bone exposed", r"vision loss"
]

PROHIBITED_SCOPES = [
    r"\bprescribe\b", r"\bdosage\b", r"\bdiagnose\b", r"\bwhich antibiotic\b",
    r"\bwhich drug\b", r"\bmg\b", r"\bmedication plan\b"
]

def is_emergency(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in EMERGENCY_PATTERNS)

def requires_professional(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in PROHIBITED_SCOPES)
