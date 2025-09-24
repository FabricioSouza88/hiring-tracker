from typing import Dict
from typing import List
from domain.interfaces.llm_client import LLMClient, Message
import appconfig
from openai import OpenAI

ALLOWED_ROLES = {"system", "user", "assistant", "tool"}

class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        self.api_key = appconfig.OPENAI_API_KEY
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def generate(
        self,
        messages: List[Message],
        model: str = None,
        temperature: float = 0.2,
        max_tokens: int = 1000
    ) -> str:
        response = self.client.chat.completions.create(
            model=model or self.model,
            messages=normalize_and_validate_messages(messages),
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return (response.choices[0].message.content or "").strip()

def normalize_and_validate_messages(messages: List[Message]) -> List[Dict[str, str]]:
    """
    - lower() em roles
    - remove mensagens sem conteúdo
    - valida roles
    - exige ao menos uma 'user'
    - exige que a última seja 'user'
    """
    norm: List[Dict[str, str]] = []
    for m in messages:
        role = (m.role or "").strip().lower()
        if role not in ALLOWED_ROLES:
            raise ValueError(f"Invalid role: {m.role!r}. Must be one of {ALLOWED_ROLES}.")
        content = (m.content or "").strip()
        if not content:
            continue
        norm.append({"role": role, "content": content})

    if not any(msg["role"] == "user" for msg in norm):
        raise ValueError("Prompt must include at least one 'user' message.")

    if norm[-1]["role"] != "user":
        raise ValueError("The last message must be from 'user' so the model can reply meaningfully.")

    return norm
