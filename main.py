import typer

from src.assistant import handle_assistant_request

app = typer.Typer()

@app.command()
def ask(query: str):
    handle_assistant_request(query)


if __name__ == "__main__":
    app()
