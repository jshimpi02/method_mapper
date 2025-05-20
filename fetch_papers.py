# fetch_papers.py
import requests

def search_semantic_scholar(goal, limit=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={goal}&fields=title,abstract,url&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [paper['abstract'] for paper in data.get('data', []) if paper.get('abstract')]
    else:
        return []