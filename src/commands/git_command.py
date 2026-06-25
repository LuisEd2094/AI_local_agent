from src.run_command import run_command
from src.commands.readme_command import generate_docs_from_content, save_docs
from typing import Any, Mapping



def build_git_diff_command(params: Mapping[str, Any]) -> list[str]:
    command = ["git", "diff"]

    if params.get("staged"):
        command.append("--staged")
    if params.get("commit1"):
        command.append(params["commit1"])
    if params.get("commit2"):
        command.append(params["commit2"])
    if params.get("file"):
        command.extend(["--", params["file"]])

    return command


def handle_git_diff(params: Mapping[str, Any], user_prompt: str | None = None) -> None:
    command = build_git_diff_command(params)

    output = run_command(command)
    print("\n--- Diff Output ---")
    print(output if output else "(Empty diff)")

    if output.strip():
        generate_docs = input("\n📝 Generate documentation from this diff? (y/n): ").strip().lower()
        if generate_docs == "y":
            save_docs(generate_docs_from_content(output, "diff", user_prompt=user_prompt))
    else:
        print("No changes to document.")