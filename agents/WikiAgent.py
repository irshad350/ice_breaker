from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_ollama import ChatOllama

from tools.tavily import get_wikipedia_urls

load_dotenv()

def lookup(topic: str, llm: ChatOllama) -> str:
    # Prompt tells LLM to choose the best Wikipedia article from a list
    template = """Use the 'tavily search' tool to find multiple Wikipedia URLs for the given topic.
                    Your job is to pick the **most relevant Wikipedia article URL** for the topic.
                    Return only that single best URL.
                    
                    Topic: "{topic_to_search}"
                """

    prompt = PromptTemplate(input_variables=["topic_to_search"], template=template)

    tools_for_agent = [
        Tool(
            name="tavily search",
            func=get_wikipedia_urls,
            description="Returns a list of Wikipedia URLs relevant to a topic. Input should be a topic name.",
        )
    ]

    # Pull ReAct prompt
    react_prompt = hub.pull("hwchase17/react")

    # Create ReAct agent
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    # Agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    # Format prompt string
    input_prompt = prompt.format_prompt(topic_to_search=topic).to_string()

    # Invoke the agent
    result = agent_executor.invoke(input={"input": input_prompt})

    output = result.get("output", "")
    print("Search result is ->", output)

    # Clean title
    if "en.wikipedia.org/wiki/" in output:
        page_title = output.split("/wiki/")[-1]
        if page_title.startswith("Category:"):
            page_title = page_title.replace("Category:", "", 1).strip()
        return page_title
    else:
        return "No Wikipedia page found."

