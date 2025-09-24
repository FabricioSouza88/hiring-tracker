import pytest
import asyncio
from agents.core.settings import get_settings

@pytest.mark.asyncio
async def test_settings_defaults():
    s = get_settings()
    assert s.prefetch == 16
    assert s.concurrency == 32
