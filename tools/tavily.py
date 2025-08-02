from langchain_tavily import TavilySearch


def get_wikipedia_page_name(topic: str):
    """Search the topic and get the wikipedia url"""
    search = TavilySearch(
        max_results=5,
        topic="general",
        # include_answer=False,
        # include_raw_content=False,
        # include_images=False,
        # include_image_descriptions=False,
        # search_depth="basic",
        # time_range="day",
        # include_domains=None,
        # exclude_domains=None
    )

    return search.invoke({"query": topic})