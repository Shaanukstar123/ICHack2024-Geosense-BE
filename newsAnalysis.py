import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from summariser.summariser import summarise_text

def update_json_with_summaries(articles):
    """
    Update the list of articles with summaries.
    """
    futures = []
    with ThreadPoolExecutor(max_workers=3) as executor:  # threading agents
        for article in articles:
            futures.append(executor.submit(summarise_text, article['content']))
            print(article['content'])

        for future, article in zip(as_completed(futures), articles):
            print(future.result())
            article['summary'] = future.result()

llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), model="gpt-3.5-turbo-0125")

output_parser = StrOutputParser()

file = open("./output.json", encoding="utf8")
input = json.load(file)
file.close()

titles = [{"id": article["id"], "title": article["title"]} for article in input]
filterPrompt = ChatPromptTemplate.from_messages([
    ("system", "Filter this list to only include entries which could have any geopolitical impact on the price of oil."),
    ("user", "{filterInput}"+"output in original json format.")
])
filterChain = filterPrompt | llm | output_parser

filterOut = filterChain.invoke({"filterInput": json.dumps(titles)})
# print(filterOut)
filteredList = json.loads(filterOut)
# print(filteredList)
filteredIndexes = [int(article["id"]) for article in filteredList]
print(filteredIndexes)
filteredInputList = [article for article in input if article["id"] in filteredIndexes]
print(len(filteredInputList))
with open('filtered_output.json', 'r', encoding='utf-8') as file:
    filtered_articles = json.load(file)
update_json_with_summaries(filtered_articles)

filteredInput = json.dumps(filteredInputList)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Give me geopolitical sentiment indexes to 3 decimal places ranging from -1 to 1 continuous values for a financial analyst interested in oil."),
    ("system", "Give me the countries that each sentiment is referring to. Provide the output in JSON form id: , countries: [], sentiment indexes: []"),
    ("user", "{input}")
])
chain = prompt | llm | output_parser

output = chain.invoke({"input": filteredInput})

print(output)