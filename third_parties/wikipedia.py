import wikipediaapi


wiki_wiki = wikipediaapi.Wikipedia(user_agent='Ai Summary Project', language='en')

def get_wiki_full_text(search_term: str) -> str:
    """
    search search_term in wikipedia and return full text from wikipedia
    """
    page_py = wiki_wiki.page(search_term)
    print("Page - Exists: %s" % page_py.exists())

    # print("Page - URL: %s" % page_py.fullurl)

    # print("Page - Summary: %s" % page_py.summary)

    return page_py.text