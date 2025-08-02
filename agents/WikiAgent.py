from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_ollama import ChatOllama

from tools.tavily import get_wikipedia_page_name

load_dotenv()

def lookup(topic: str) -> str:
    llm = ChatOllama(model="gemma3")

    template = """Return the exact Wikipedia page title for the following topic. Do not include any explanation or formatting, only the title string.
                    Topic: {topic_to_search}."""

    prompt = PromptTemplate(input_variables=["topic_to_search"], template=template)

    tools_for_agent = [
        Tool(
            name="Wikipedia page name search",
            func=get_wikipedia_page_name,
            description="useful for when you need get the wikipedia page name",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt.format_prompt(topic_to_search=topic)},
    )

    wiki_title = result
    return wiki_title


# if __name__ == '__main__':
#     print("Hello LangChain!")
#
#     res = lookup(topic="Python_(programming_language)")
#
#     print(res)

