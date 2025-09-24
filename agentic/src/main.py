"""
Main entry point for the agentic application.
This runs a polling loop that continuously checks for new tasks to process.
It uses the RouterAgent to delegate tasks to the appropriate sub-agents
based on the current evaluation stage (e.g., TRIAGE, TEST, REPORT).
"""

import time
import logging

from core.logging_setup import setup_logging
from agents.router.router_agent import RouterAgent
import appconfig

# --- Polling loop ------------------------------------------------------------

def main() -> None:
    setup_logging(appconfig.LOG_LEVEL)
    logging.info("Starting polling loop (API-driven)…")

    router = RouterAgent()

    while True:
        try:
            # One tick attempts TRIAGE -> TEST -> REPORT in priority order,
            # processing at most one item, and returns True if something was processed.
            processed = router.run_tick()
        except Exception as ex:
            logging.error(f"Tick failed: {ex}", exc_info=True)
            processed = False

        # If we processed an item, we shorten the next sleep to re-check sooner.
        time.sleep(10 if processed else appconfig.POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
