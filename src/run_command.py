import shlex
import subprocess

def format_command(command: list[str]) -> str:
    return " ".join(shlex.quote(argument) for argument in command)


def run_command(command: list[str]) -> str:
    print(f"\n🔍 I want to run: {format_command(command)}")

    confirm = input("Run this command? (y/n): ").strip().lower()
    if confirm != "y":
        print("⏹️  Cancelled.")
        return
    return subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)