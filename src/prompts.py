from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "promts"

def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8").strip()


SYSTEM_PROMPT = load_prompt("system_prompt.txt")
DIFF_PROMPT_TEMPLATE = load_prompt("diff_promt.txt")
FILE_PROMPT_TEMPLATE = load_prompt("file_promt.txt")
FOLDER_PROMPT_TEMPLATE = load_prompt("folder_promt.txt")


def build_document_prompt(
        content: str,
        content_type: str = "diff",
        filename: str | None = None,
        folderpath: str | None = None,
        ) -> str:
    if content_type == "diff":
        return DIFF_PROMPT_TEMPLATE.format(content=content)
    if content_type == "file":
        return FILE_PROMPT_TEMPLATE.format(content=content, filename=filename or "this file")
    if content_type == "folder":
        if not isinstance(content, dict):
            raise TypeError("content must be dict for folder")
        files_content = ""
        for rel_path, file_content in content.items():
            files_content += f"\n### File: {rel_path}\n\n```\n{file_content}\n```\n"
        return FOLDER_PROMPT_TEMPLATE.format(
            folderpath=folderpath or ".",
            content=files_content
        )

    raise ValueError(f"Unsupported content type: {content_type}")