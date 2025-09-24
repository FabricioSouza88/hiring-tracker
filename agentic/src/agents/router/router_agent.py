import logging
from typing import Optional
from agents.router.types import GET_NEXT_ENDPOINT, UPDATE_REPORT_ENDPOINT
from domain.enums.eval_stage_enum import EvalStage
from client.api_client import get_next, update_status, post_report
from domain.models.models import TriageTask, RoleApplication, TriageReportPayload
from agents.triage.triage_agent import TriageAgent
from domain.interfaces.llm_client import LLMClient
from mcp.mcp_tools import MCPTools, NoopMCPTools
import appconfig

class RouterAgent:
    """
    Pulls one item per tick, in stage priority order.
    On each tick, tries TRIAGE -> TEST -> REPORT and processes the first available.
    """

    def __init__(self, llm: LLMClient, tools: MCPTools | None = None) -> None:
        self.triage_agent = TriageAgent(llm=llm, tools=tools or NoopMCPTools())
        # self.test_agent = TestAgent()      # quando existir
        # self.report_agent = ReportAgent()  # quando existir

    def run_tick(self) -> bool:
        # priority order
        for stage in (EvalStage.TRIAGE, EvalStage.TEST, EvalStage.REPORT):
            processed = self._try_stage(stage)
            if processed:
                return True
        return False

    def _try_stage(self, stage: EvalStage) -> bool:
        endpoint = GET_NEXT_ENDPOINT[stage]
        raw = get_next(endpoint)
        if not raw:
            logging.debug(f"No pending items for stage={stage.value}")
            return False

        # Por enquanto, temos o contrato TriageTask; para os demais, você criará equivalentes.
        task = TriageTask(**raw)
        logging.info(f"Picked {stage.value} task_id={task.task_id} candidate={task.candidate_id}")

        # status "started"
        try:
            update_status(task.task_id, f"evaluating{stage.value.capitalize()}")
        except Exception as ex:
            logging.error(f"Failed to UpdateStatus start stage={stage.value}: {ex}")
            return False

        # roteia para o agente correto
        if stage is EvalStage.TRIAGE:
            return self._handle_triage(task)
        # elif stage is EvalStage.TEST:
        #     return self._handle_test(task)
        # elif stage is EvalStage.REPORT:
        #     return self._handle_report(task)
        else:
            logging.warning(f"Stage not implemented: {stage.value}")
            return False

    def _handle_triage(self, task: TriageTask) -> bool:
        role_application = RoleApplication(**task.payload["role_application"])
        result, artifacts = self.triage_agent.evaluate(role_application)

        report = TriageReportPayload(
            task_id=task.task_id,
            tenant_id=task.tenant_id,
            candidate_id=task.candidate_id,
            result=result,
            artifacts=artifacts
        )

        # envia o relatório para a API
        post_report(UPDATE_REPORT_ENDPOINT[EvalStage.TRIAGE], report.model_dump())
        logging.info(f"Triage complete task_id={task.task_id} decision={result.triage_decision} score={result.triage_score} triage_feedback={result.triage_feedback}")

        # status final (opcional)
        if appconfig.UPDATE_STATUS_ON_COMPLETE:
            try:
                update_status(task.task_id, "triageEvaluated")
            except Exception as ex:
                logging.warning(f"Final UpdateStatus failed (non-blocking): {ex}")

        return True

    # def _handle_test(self, task: TestTask) -> bool:
    #     ...
    # def _handle_report(self, task: ReportTask) -> bool:
    #     ...
