from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json, os

llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), model="gpt-3.5-turbo-0125")

output_parser = StrOutputParser()

file = open("./webCrawler/output.json", encoding="utf8")
input = json.load(file)
file.close()

titles = [{"id": article["id"], "title": article["title"]} for article in input]
filterPrompt = ChatPromptTemplate.from_messages([
    ("system", "Filter this list to only include entries which could have any geopolitical impact on the price of oil."),
    ("user", "{filterInput}"+"output in original json format.")
])
filterChain = filterPrompt | llm | output_parser

filterOut = filterChain.invoke({"filterInput": json.dumps(titles)})
print(filterOut)
filteredList = json.loads(filterOut)
print(filteredList)
filteredIndexes = [int(article["id"]) for article in filteredList]
print(filteredIndexes)
filteredInput = json.dumps([article for article in input if article["id"] in filteredIndexes])

prompt = ChatPromptTemplate.from_messages([
    ("system", "Give me geopolitical sentiment indexes to 3 decimal places ranging from -1 to 1 continuous values for a financial analyst interested in oil."),
    ("system", "Give me the countries that each sentiment is referring to. Provide the output in JSON form id: , countries: [], sentiment indexes: []"),
    ("user", "{input}")
])
chain = prompt | llm | output_parser

output = chain.invoke({"input": filteredInput})

print(output)