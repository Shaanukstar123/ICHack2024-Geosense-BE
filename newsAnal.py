from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json, os

llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), model="gpt-3.5-turbo-0125")

output_parser = StrOutputParser()

file = open("./webCrawler/output.json")
input = json.load(file)
file.close()

titles = [[article["id"], article["title"]] for article in input]
filterPrompt = ChatPromptTemplate.from_messages([
    ("system", "Filter this list to only include entries which could have any geopolitical impact on the price of oil."),
    ("user", "{filterInput}"+"output in original json format.")
])
filterChain = filterPrompt | llm | output_parser

filteredOutput = filterChain.invoke({"filterInput": titles})

print(filteredOutput)
# summaries = []
# for article_id in articles:
    # print(article_id)
    
#     summary = "summariser/summariser.py".summarise_text(article_id)  # Use your summarise_text function
#     summaries.append(summary)

# TODO: Take the filtered list and get the full articles back then iterate through all of them and feed them to the LLM
# for 




# prompt = ChatPromptTemplate.from_messages([
#     ("system", "Give me geopolitical sentiment indexes to 3 decimal places ranging from -1 to 1 continuous values for a financial analyst interested in oil."),
#     ("system", "Give me the countries that each sentiment is referring to. Provide the output in JSON form id: , countries: [], sentiment indexes: []"),
#     ("user", "{input}")
# ])
# chain = prompt | llm | output_parser

# output = chain.invoke({"input": filteredOutput})

# output
