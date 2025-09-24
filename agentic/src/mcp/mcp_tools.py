# src/agent/mcp_tools.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class MCPTools(ABC):
    """Abstract MCP tools client (e.g., FastAPIMCP)."""
    @abstractmethod
    def fetch_linkedin(self, url: str) -> Optional[Dict[str, Any]]:
        ...
    @abstractmethod
    def fetch_github(self, url: str) -> Optional[Dict[str, Any]]:
        ...
    @abstractmethod
    def fetch_portfolio(self, url: str) -> Optional[Dict[str, Any]]:
        ...

class NoopMCPTools(MCPTools):
    """Fallback that returns None for everything."""
    def fetch_linkedin(self, url: str) -> Optional[Dict[str, Any]]: return None
    def fetch_github(self, url: str) -> Optional[Dict[str, Any]]: return None
    def fetch_portfolio(self, url: str) -> Optional[Dict[str, Any]]: return None
