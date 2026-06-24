import typer

from src.assistant import handle_assistant_request

app = typer.Typer()

@app.callback()
def main():
    """Root entry point – no action."""
    pass

@app.command("ask")
def ask(query: str):
    handle_assistant_request(query)

if __name__ == "__main__":
    app()
