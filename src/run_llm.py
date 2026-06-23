from .contants import MODEL

import ollama
import json
import re

def call_llm(messages, expect_json=False, temperature=0.1, **kwargs):
    """
    Send messages to the local LLM.
    - expect_json: if True, forces JSON output and parses it.
    - Additional kwargs (temperature, max_tokens, etc.) are passed through.
    Returns parsed JSON dict if expect_json=True, otherwise raw text string.
    """
    default_params = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {'temperature': temperature},

    }
    if expect_json:
        default_params["format"] = "json"

    params = {**default_params, **kwargs}
    response = ollama.chat(**params)
    content = response["message"]["content"]

    if expect_json:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise ValueError("No valid JSON found in response")
    else:
        return content