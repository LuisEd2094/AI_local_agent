import os

from src.run_command import run_command
from src.run_llm import call_llm
from src.prompts import build_document_prompt
from pathlib import Path
from typing import Any, Mapping


def generate_docs_from_content(
        content: str,
        content_type: str = "diff", 
        max_chars: int = 4000,
        filename: str | None = None,
    ) -> str:
    prompt = build_document_prompt(content, content_type=content_type, max_chars=max_chars, filename=filename)
    return call_llm(
        messages=[
            {"role": "system", "content": "You produce high-quality Markdown documentation."},
            {"role": "user", "content": prompt},
        ],
        expect_json=False,
        options={"temperature": 0.4},
    )


def handle_generate_readme(params: Mapping[str, Any]) -> None:
    source = params.get("source")

    if source == "git_diff":
        print("🔍 Running git diff to fetch changes...")
        diff_output = run_command(["git", "diff"])
        if not diff_output.strip():
            print("No diff found.")
            return
        save_docs(generate_docs_from_content(diff_output, "diff"))
        return

    if source == "file":
        filepath = params.get("filepath")
        if not filepath:
            print("❌ Missing 'filepath' parameter.")
            return

        if not os.path.isfile(filepath):
            print(f"❌ File not found: {filepath}")
            return

        print(f"🔍 Reading file: {filepath}")
        content = Path(filepath).read_text(encoding="utf-8")
        save_docs(generate_docs_from_content(content, "file", filename=filepath))
        return

    print(f"❌ Unknown source: {source}")


def save_docs(content: str, default_filename: str = "README.md") -> None:
    print("\n--- Generated Documentation ---")
    print(content)
    print("-------------------------------")

    filename = input(f"💾 Save to file (default: {default_filename}): ").strip() or default_filename
    if os.path.exists(filename):
        overwrite = input(f"⚠️  {filename} exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != "y":
            print("❌ Not saved.")
            return

    Path(filename).write_text(content, encoding="utf-8")
    print(f"✅ Documentation saved to {filename}")