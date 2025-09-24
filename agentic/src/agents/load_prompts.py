from pathlib import Path

def load_prompt(scope: str, prompt_name: str, fallback: str = "") -> str:
    """
    Load a prompt file from the prompts directory based on the given scope and prompt name.
    Args:
        scope (str): The scope or category of the prompt (e.g., "triage").
        prompt_name (str): The name of the prompt file (e.g., "triage_system.md").
        fallback (str): The fallback string to return if the prompt file is not found.
    Returns:
        str: The content of the prompt file or the fallback string.
    """
    try:
        p = Path(__file__).parent / scope / "prompts" / prompt_name
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return fallback