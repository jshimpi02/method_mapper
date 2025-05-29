# generator.py — now using Hugging Face Inference API (Mistral)
import os
import pandas as pd
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
HUGGINGFACE_API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 512,
            "return_full_text": False
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()[0]["generated_text"]


def extract_methods_table(research_goal):
    prompt = f"""
Given the research goal: "{research_goal}", extract a table of:
1. Method used
2. Tools or software (if mentioned)
3. Datasets (if mentioned)
4. Evaluation metrics (e.g., accuracy, F1)
Return a structured JSON list like this:
[
  {{"Method": "...", "Tools": "...", "Dataset": "...", "Metrics": "..."}},
  ...
]
"""
    try:
        raw_output = query_huggingface(prompt)
        table = eval(raw_output.strip())  # ⚠️ Assumes trusted JSON-like output
        return pd.DataFrame(table)
    except Exception as e:
        print("Failed to extract methods table:", e)
        return pd.DataFrame()


def extract_methods_from_pdf(file):
    import fitz  # PyMuPDF
    import pandas as pd

    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    prompt = f"""
Extract methods used in this study from the following text:
{text[:3000]}...
Return a structured JSON list with Method, Tools, Dataset, Metrics.
"""
    try:
        raw_output = query_huggingface(prompt)
        table = eval(raw_output.strip())
        return pd.DataFrame(table)
    except Exception as e:
        print("PDF extraction failed:", e)
        return pd.DataFrame()
