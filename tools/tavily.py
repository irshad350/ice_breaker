from langchain_tavily import TavilySearch

def get_wikipedia_urls(topic: str) -> str:
    """Search the topic and return all relevant Wikipedia URLs as a list of strings."""
    search = TavilySearch(
        max_results=10,
        topic="general"
    )

    results = search.invoke({"query": topic})

    if isinstance(results, dict) and "results" in results:
        results = results["results"]

    wikipedia_links = [
        result.get("url", "")
        for result in results
        if "en.wikipedia.org/wiki/" in result.get("url", "")
        and "Category:" not in result.get("url", "")
    ]

    if not wikipedia_links:
        return "No relevant Wikipedia URLs found."

    return "\n".join(wikipedia_links)  # Return as newline-separated string for the LLM
