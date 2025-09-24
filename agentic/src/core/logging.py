import structlog

def get_logger(name: str = "agents"):
    return structlog.get_logger(name)
