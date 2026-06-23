from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "promts"

def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8").strip()


SYSTEM_PROMPT = load_prompt("system_prompt.txt")
DIFF_PROMPT_TEMPLATE = load_prompt("diff_promt.txt")
FILE_PROMPT_TEMPLATE = load_prompt("file_promt.txt")


def build_document_prompt(
        content: str,
        content_type: str = "diff",
        max_chars: int = 4000,
        filename: str | None = None,
        ) -> str:
    truncated_content = content if len(content) <= max_chars else content[:max_chars] + "\n... (truncated)"

    if content_type == "diff":
        return DIFF_PROMPT_TEMPLATE.format(content=truncated_content)
    if content_type == "file":
        return FILE_PROMPT_TEMPLATE.format(content=truncated_content, filename=filename or "this file")

    raise ValueError(f"Unsupported content type: {content_type}")