# Nome dos canais da API por estágio (read/consume)
from domain.enums.eval_stage_enum import EvalStage

GET_NEXT_ENDPOINT = {
    EvalStage.TRIAGE: "/getNextTriage",
    EvalStage.TEST:   "/getNextTest",    # sua API deve expor quando estiver pronto
    EvalStage.REPORT: "/getNextReport",  # idem
}

# Endpoints de atualização por estágio (write)
UPDATE_REPORT_ENDPOINT = {
    EvalStage.TRIAGE: "/UpdateTriageReport",
    EvalStage.TEST:   "/UpdateTestReport",
    EvalStage.REPORT: "/UpdateFinalReport",
}