import structlog

def get_logger(name: str = "api"):
    return structlog.get_logger(name)
