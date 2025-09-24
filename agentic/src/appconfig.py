import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "local")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UPDATE_STATUS_ON_COMPLETE = os.getenv("UPDATE_STATUS_ON_COMPLETE", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "10"))
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")
API_KEY = os.getenv("API_KEY", "changeme")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))
MAX_HTTP_RETRIES = int(os.getenv("MAX_HTTP_RETRIES", "5"))