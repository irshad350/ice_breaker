from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from third_parties.wikipedia import get_wiki_full_text
from agents.WikiAgent import lookup


def ice_break_with(search_name: str) -> str:
    llm = ChatOllama(model="gemma3:4b")

    # step -1 : get wiki link for given word
    wiki_topic = lookup(topic=search_name, llm=llm)

    print(wiki_topic)
    # step -2 : get full text for given url
    wiki_text = get_wiki_full_text(wiki_topic)

    summary_template = """
           given the information {information} from wikipedia i want you to create:
           1: a short summary
           2: five interesting facts about the topic
       """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    chain = summary_prompt_template | llm | StrOutputParser()

    return chain.invoke(input={"information": wiki_text})


if __name__ == '__main__':
    print("Hello LangChain!")

    print(ice_break_with(search_name='Python programming language - Wikipedia'))




