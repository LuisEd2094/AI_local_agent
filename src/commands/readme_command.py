import os

from src.run_command import run_command
from src.run_llm import call_llm
from src.prompts import build_doc_messages
from pathlib import Path
from typing import Any, Mapping

SKIP_DIRS = {'__pycache__', '.git', '.venv', '.env', 'node_modules', 'dist', 'build', '__MACOSX', 'promts'}



def generate_docs_from_content(
        content: str,
        content_type: str = "diff", 
        filename: str | None = None,
        folderpath: str | None = None,
        user_prompt: str | None = None

    ) -> str:
    system_prompt, user_message = build_doc_messages(
        content=content,
        content_type=content_type,
        filename=filename,
        folderpath=folderpath,
        user_prompt=user_prompt,
    )
    print(f"\n🔍 Generating documentation with prompt:{user_message}")
    return call_llm(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        expect_json=False,
        options={"temperature": 0.1},
    )

def read_file_content(filepath: str) -> str:
    if not filepath or not os.path.isfile(filepath):
        raise ValueError(f"File not found: {filepath}")
    try:
        content = Path(filepath).read_text(encoding='utf-8')
        return content
    except Exception as e:
        raise ValueError(f"Could not read file {filepath}: {e}")

def read_folder_files(
    folderpath: str,
    extensions: tuple = ('.py', '.md', '.txt', '.json', '.yaml', '.js', '.html', '.css'),
    include_hidden: bool = False
) -> dict[str, str]:
    """
    Read all files in a folder (recursively) and return a dict {filename: content}.
    
    Raises:
        ValueError: if folderpath is empty, does not exist, or is not a directory.
    """
    if not folderpath:
        raise ValueError("Folder path is empty.")
    if not os.path.exists(folderpath):
        raise ValueError(f"Folder does not exist: {folderpath}")
    if not os.path.isdir(folderpath):
        raise ValueError(f"Path is not a directory: {folderpath}")

    contents = {}
    root = Path(folderpath)
    for filepath in root.rglob('*'):
        if not include_hidden:
            if any(part.startswith('.') for part in filepath.parts):
                continue
        if any(part in SKIP_DIRS for part in filepath.parts):
            continue
        print(f"🔍 Checking file: {filepath}")
        if filepath.is_file() and filepath.suffix in extensions:
            try:
                content = read_file_content(filepath)
                contents[str(filepath.relative_to(root))] = content
            except ValueError as e:
                contents[str(filepath.relative_to(root))] = f"(Error reading file: {e})"
    return contents

def handle_generate_readme(params: Mapping[str, Any],
                           user_prompt: str | None = None) -> None:
    source = params.get("source")
    if source is None:
        print("❌ Missing 'source' parameter.")
        return
    doc = None
    additional_context = params.get("additional_context", False)

    if source == "git_diff":
        print("🔍 Running git diff to fetch changes...")
        diff_output = run_command(["git", "diff"])
        if not diff_output.strip():
            print("No diff found.")
            return
        doc = generate_docs_from_content(diff_output, "diff", user_prompt=user_prompt)

    elif source == "file":
        filepath = params.get("filepath")
        print(f"🔍 Reading file: {filepath}")
        content = read_file_content(filepath)
        doc = generate_docs_from_content(content, "file", filename=filepath, user_prompt=user_prompt)

    elif source == "folder":
        folderpath = params.get("folderpath")
        if not folderpath:
            print("❌ Missing 'folderpath' parameter.")
            return

        try:
            if additional_context:
                print("🔍 Reading whole repository for context...")
                contents = read_folder_files(".")
            else:
                print(f"🔍 Reading folder: {folderpath}")
                contents = read_folder_files(folderpath)
        except ValueError as e:
            print(f"❌ {e}")
            return

        if not contents:
            print("❌ No readable files found.")
            return

        doc = generate_docs_from_content(
            contents,
            content_type="folder",
            folderpath=folderpath,
            user_prompt=user_prompt,
        )
    else:
        print(f"❌ Unknown source: {source}")
        return
    if not doc:
        print("❌ No documentation generated.")
        return

    save_docs(doc)

def save_docs(content: str, default_filename: str = "AGENT_RESULT.md") -> None:
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