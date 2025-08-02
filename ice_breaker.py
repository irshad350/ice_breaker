from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from third_parties.wikipedia import get_wiki_full_text
from agents.WikiAgent import lookup


def ice_break_with(search_name: str) -> str:
    # step -1 : get wiki link for given word
    wiki_topic = lookup(topic=search_name)

    # step -2 : get full text for given url
    wiki_text = get_wiki_full_text(wiki_topic)

    summary_template = """
           given the information {information} from wikipedia i want you to create:
           1: a short summary
           2. five interesting facts about the topic
       """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    llm = ChatOllama(model="gemma3")

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": wiki_text})

    print(res)

if __name__ == '__main__':
    print("Hello LangChain!")
    ice_break_with(search_name='Python programming language')




