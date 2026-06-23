import typer
import ollama

app = typer.Typer()
MODEL = "qwen3:8b"
SYSTEM_PROMT = (
        "You are a helpful assistant that can answer questions and assist with "
        "software development tasks. Keep responses clear and concise."
    )

@app.command()
def ask(query: str):
    """
    Send a natural language query to the local AI assistant and get a response.
    """
    try:
        stream = ollama.chat(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMT},
                    {"role": "user", "content": query},
                ],
                stream=True,
            )
        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)
    except Exception as e:
        print(f"Error calling Ollama: {e}")

if __name__ == "__main__":
    app()