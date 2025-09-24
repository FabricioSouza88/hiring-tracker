import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def db_session_mock():
    class Sess(AsyncMock):
        async def flush(self): pass
        async def close(self): pass
    return Sess()
