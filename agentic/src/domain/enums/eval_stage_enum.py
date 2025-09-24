from enum import Enum

class EvalStage(str, Enum):
    TRIAGE = "triage"
    TEST = "test"
    REPORT = "report"