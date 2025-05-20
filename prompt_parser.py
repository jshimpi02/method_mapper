# parser.py
import subprocess
import json

def format_prompt(abstracts):
    combined_text = "\n\n".join(abstracts)
    return f"""
You are an expert scientific assistant. Given the following research abstracts, extract a structured table with the following fields:
- Method
- Tools/Software
- Dataset
- Metrics
- Subfield/Domain

Respond in valid JSON list format like:
[
  {{"Method": ..., "Tools": ..., "Dataset": ..., "Metrics": ..., "Domain": ...}},
  ...
]

Abstracts:
{combined_text}
"""

def call_llama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout
    except Exception as e:
        print(f"Error calling LLaMA: {e}")
        return "[]"

def parse_llama_output(output):
    try:
        return json.loads(output.strip())
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}\nRaw output: {output}")
        return []
