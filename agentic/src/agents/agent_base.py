from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from domain.interfaces.llm_client import LLMClient, Message
from mcp.mcp_tools import MCPTools, NoopMCPTools
from agents.load_prompts import load_prompt


class AgentBase(ABC):
    """
    Base class for all agents providing common functionality for:
    - LLM client integration
    - MCP tools integration
    - Prompt loading and management
    - Safe template formatting
    """
    
    def __init__(self, llm: LLMClient, tools: MCPTools | None = None, scope: str = "") -> None:
        self.llm = llm
        self.tools = tools or NoopMCPTools()
        self.scope = scope
        self._prompts: Dict[str, str] = {}
    
    def _load_prompt(self, filename: str, fallback: str = "") -> str:
        """
        Load a prompt from the scope directory with fallback handling.
        
        Args:
            filename: Name of the prompt file
            fallback: Default value if loading fails
            
        Returns:
            Loaded prompt content or fallback
        """
        try:
            prompt = load_prompt(self.scope, filename)
            self._prompts[filename] = prompt
            return prompt
        except Exception:
            self._prompts[filename] = fallback
            return fallback
    
    def _safe_format(self, template: str, context: Dict[str, Any]) -> str:
        """
        Safely format template with fallback for missing keys.
        
        Args:
            template: Template string to format
            context: Context dictionary for formatting
            
        Returns:
            Formatted string with safe fallbacks
        """
        class SafeDict(dict):
            def __missing__(self, key):
                return ""
        
        return template.format_map(SafeDict(context))
    
    def _generate_llm_response(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        temperature: float = 0.2, 
        max_tokens: int = 1000
    ) -> str:
        """
        Generate LLM response with system and user prompts.
        
        Args:
            system_prompt: System prompt for context
            user_prompt: User prompt for the task
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response text
        """
        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content=user_prompt),
        ]
        response = self.llm.generate(messages, temperature=temperature, max_tokens=max_tokens)
        return response.strip()
    
    def _safe_getattr(self, obj: Any, attr: str, default: Any = "") -> Any:
        """
        Safely get attribute from object with fallback.
        
        Args:
            obj: Object to get attribute from
            attr: Attribute name
            default: Default value if attribute doesn't exist
            
        Returns:
            Attribute value or default
        """
        return getattr(obj, attr, default)
    
    def _safe_join_list(self, obj: Any, attr: str, separator: str = ", ") -> str:
        """
        Safely join list attribute from object.
        
        Args:
            obj: Object to get list attribute from
            attr: List attribute name
            separator: Separator for joining
            
        Returns:
            Joined string or empty string if attribute doesn't exist
        """
        items = getattr(obj, attr, []) or []
        return separator.join(items) if items else ""
    
    @abstractmethod
    def evaluate(self, *args, **kwargs) -> Any:
        """
        Abstract method for agent evaluation.
        Must be implemented by subclasses.
        """
        pass