# generator.py
import requests
import pandas as pd
import subprocess
import json
import re
import fitz  # PyMuPDF

def search_semantic_scholar(goal, limit=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={goal}&fields=title,abstract,url&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [paper['abstract'] for paper in data.get('data', []) if paper.get('abstract')]
    else:
        print("Semantic Scholar API error:", response.status_code, response.text)
        return []

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

Only output the JSON list.

Abstracts:
{combined_text}
"""

def call_llama(prompt):
    try:
        process = subprocess.Popen(
            ["ollama", "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=prompt, timeout=120)

        if stderr:
            print("LLaMA stderr:", stderr)

        return stdout
    except Exception as e:
        print(f"Error calling LLaMA: {e}")
        return "[]"

def extract_methods_table(goal):
    abstracts = search_semantic_scholar(goal)
    print(f"Fetched {len(abstracts)} abstracts.")
    if not abstracts:
        return pd.DataFrame([])

    prompt = format_prompt(abstracts)
    print("=== Prompt Sent to LLaMA ===")
    print(prompt)
    print("=============================")

    output = call_llama(prompt)

    print("---- LLaMA Raw Output ----")
    print(output)
    print("--------------------------")

    try:
        data = json.loads(output.strip())
    except json.JSONDecodeError:
        match = re.search(r"\[\s*{.*?}\s*\]", output, re.DOTALL)
        if match:
            json_text = match.group(0)
            try:
                data = json.loads(json_text)
            except Exception as e:
                print("Fallback JSON parse error:", e)
                data = []
        else:
            print("No valid JSON array found in output.")
            data = []

    return pd.DataFrame(data)

def extract_methods_from_pdf(uploaded_file):
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])
        if len(text.strip()) < 100:
            print("PDF contains too little readable text.")
            return pd.DataFrame([])

        prompt = f"""
You are an expert scientific assistant. Given the following research paper text, extract a structured table with the following fields:
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

Only output the JSON list.

Text:
{text[:4000]}
"""  # Truncate to 4000 chars

        output = call_llama(prompt)
        print("LLaMA PDF Output:", output)

        try:
            return pd.DataFrame(json.loads(output.strip()))
        except json.JSONDecodeError:
            match = re.search(r"\[\s*{.*?}\s*\]", output, re.DOTALL)
            if match:
                return pd.DataFrame(json.loads(match.group(0)))
            else:
                print("No valid JSON array found in PDF output.")
                return pd.DataFrame([])

    except Exception as e:
        print(f"PDF processing error: {e}")
        return pd.DataFrame([])
