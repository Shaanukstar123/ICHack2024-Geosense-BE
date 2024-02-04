from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

llm = ChatOpenAI(openai_api_key="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")
output_parser = StrOutputParser()

file = open("testInput.json")
input = json.load(file)
file.close()

titles = [[article["id"], article["title"]] for article in input]
filterPrompt = ChatPromptTemplate.from_messages([
    ("system", "Filter this list to only include entries which could have any geopolitical impact on the price of oil."),
    ("user", "{filterInput}")
])
filterChain = filterPrompt | llm | output_parser

filteredOutput = filterChain.invoke({"filterInput": titles})

# TODO: Take the filtered list and get the full articles back then iterate through all of them and feed them to the LLM

prompt = ChatPromptTemplate.from_messages([
    ("system", "Give me geopolitical sentiment indexes to 3 decimal places ranging from -1 to 1 continuous values for a financial analyst interested in oil."),
    ("system", "Give me the countries that each sentiment is referring to. Provide the output in JSON form id: , countries: [], sentiment indexes: []"),
    ("user", "{input}")
])
chain = prompt | llm | output_parser

output = chain.invoke({"input": "id: 543, content: Ireland will leave the union, and Scotland could too. True devolution is the only way to save it."})

print(output)
