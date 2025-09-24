from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class Message:
    role: str  # "system" | "user" | "assistant"
    content: str

class LLMClient(ABC):
    """Abstract LLM client; implement with OpenAI, Azure, or Vertex."""
    @abstractmethod
    def generate(self, messages: List[Message], temperature: float = 0.2, max_tokens: int = 1000) -> str:
        ...