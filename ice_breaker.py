from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from third_parties.wikipedia import get_wiki_full_text


topic = 'Python_(programming_language)'

if __name__ == '__main__':
    print("Hello LangChain!")

    summary_template = """
        given the information {information} from wikipedia i want you to create:
        1: a short summary
        2. two interesting facts about th
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    llm = ChatOllama(model="gemma3")

    chain = summary_prompt_template | llm | StrOutputParser()

    wiki_text = get_wiki_full_text(topic)

    res = chain.invoke(input={"information": wiki_text})

    print(res)
