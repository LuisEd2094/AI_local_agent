from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "promts"

def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8").strip()


MAIN_SYS = load_prompt("main_system.txt")

DOC_PROMPTS = {
    "diff": {
        "system": "system_diff.txt",
        "user": "user_diff.txt",
    },
    "file": {
        "system": "system_file.txt",
        "user": "user_file.txt",
    },
    "folder": {
        "system": "system_folder.txt",
        "user": "user_folder.txt",
    },
}


def build_doc_messages(
    content: str | dict[str, str],
    content_type: str,
    filename: str | None = None,
    folderpath: str | None = None,
    user_prompt: str | None = None,
) -> tuple[str, str]:
    """
    Build system and user messages for documentation generation.
    Returns (system_prompt, user_message).
    """
    if content_type not in DOC_PROMPTS:
        raise ValueError(f"Unsupported content type: {content_type}")

    system_prompt = load_prompt(DOC_PROMPTS[content_type]["system"])
    user_template = load_prompt(DOC_PROMPTS[content_type]["user"])

    if content_type == "folder":
        if not isinstance(content, dict):
            raise TypeError("content must be dict for folder")
        files_content = ""
        for rel_path, file_content in content.items():
            files_content += f"\n### File: {rel_path}\n\n```\n{file_content}\n```\n"
        content = files_content

    user_message = user_template.format(
        content=content,
        filename=filename or "this file",
        folderpath=folderpath or ".",
        user_prompt=user_prompt or "No specific request.",
    )

    return system_prompt, user_message