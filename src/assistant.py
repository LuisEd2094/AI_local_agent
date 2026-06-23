from __future__ import annotations
import time

from src.commands.git_command import handle_git_diff
from src.commands.readme_command import handle_generate_readme
from src.run_llm import call_llm

from .prompts import SYSTEM_PROMPT


COMMANDS = {
    "git_diff": handle_git_diff,
    "generate_readme": handle_generate_readme,
}

def handle_assistant_request(query: str) -> None:
    start_time = time.time()

    try:
        result = call_llm(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            expect_json=True,
        )
        action = result.get("action")
        params = result.get("parameters", {})
        print(f"\n🤖 Assistant suggested action: {action} with parameters: {params}")

        if action in COMMANDS:
            COMMANDS[action](params)
        else:
            print(f"⚠️  Unknown action: {action}")
            
    except ValueError as error:
        print(f"❌ The assistant did not return valid JSON: {error}")
    except Exception as error:
        print(f"❌ An error occurred: {error}")
    finally:
        print(f"\n⏱️  Total time: {time.time() - start_time:.2f}s")
