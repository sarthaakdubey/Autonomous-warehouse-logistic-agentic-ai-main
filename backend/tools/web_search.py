import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str):
    results = client.search(query=query, max_results=3)
    return [r["url"] for r in results["results"]]
