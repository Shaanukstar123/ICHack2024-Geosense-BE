# import json
# import os
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from summariser.summariser import summarise_text

# def update_json_with_summaries(articles):
#     """
#     Update the list of articles with summaries, processing them sequentially.
#     """
#     for article in articles:
#         try:
#             # Call summarise_text for each article and update the 'summary' field
#             summary = summarise_text(article['content'])
#             article['summary'] = summary
#             print(article['content'])  # Optional: Print the article content for debugging
#             print(summary)  # Optional: Print the generated summary for debugging
#         except Exception as e:
#             print(f"Error summarizing article: {e}")
#             article['summary'] = "Summary unavailable due to error."

# llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), model="gpt-3.5-turbo-0125")

# output_parser = StrOutputParser()

# file = open("./output.json", encoding="utf8")
# input = json.load(file)
# file.close()

# titles = [{"id": article["id"], "title": article["title"]} for article in input]
# filterPrompt = ChatPromptTemplate.from_messages([
#     ("system", "Filter this list to only include entries which could have any geopolitical impact on the price of oil."),
#     ("user", "{filterInput}"+"output in original json format.")
# ])
# filterChain = filterPrompt | llm | output_parser

# filterOut = filterChain.invoke({"filterInput": json.dumps(titles)})
# # print(filterOut)
# filteredList = json.loads(filterOut)
# # print(filteredList)
# filteredIndexes = [int(article["id"]) for article in filteredList]
# print(filteredIndexes)
# filteredInputList = [article for article in input if article["id"] in filteredIndexes]
# print(len(filteredInputList))
# with open('filtered_output.json', 'r', encoding='utf-8') as file:
#     filtered_articles = json.load(file)
# update_json_with_summaries(filtered_articles)

# filteredInput = json.dumps(filteredInputList)

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "Give me geopolitical sentiment indexes to 3 decimal places ranging from -1 to 1 continuous values for a financial analyst interested in oil."),
#     ("system", "Give me the countries that each sentiment is referring to. Provide the output in JSON form id: , countries: [], sentiment indexes: []"),
#     ("user", "{input}")
# ])
# chain = prompt | llm | output_parser

# output = chain.invoke({"input": filteredInput})

# print(output)

import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from summariser.summariser import summarise_text

def update_json_with_summaries(articles):
    print("Starting summarization...")
    count = 0
    articles = []
    for article in articles:
        if count >= 5:
            break
        try:
            print(f"Summarizing article ID: {article['id']}")
            summary = summarise_text(article['content'])
            article['content'] = summary
            print(f"Summary for article ID: {article['id']} completed")
            articles.append(article)
            count += 1
        except Exception as e:
            print(f"Error summarizing article ID: {article['id']}: {e}")
            article['content'] = "Summary unavailable"
    return articles

print("Initializing Langchain components...")
llm = ChatOpenAI(openai_api_key=os.environ.get("OPEN_API_KEY"), model="gpt-4")
output_parser = StrOutputParser()

def update_region_sentiment():
    print("Initializing Langchain components...")
    llm = ChatOpenAI(openai_api_key='Open_AI_API', model="gpt-4")
    output_parser = StrOutputParser()

    print("Loading articles from JSON...")
    with open("./output.json", encoding="utf8") as file:
        articles = json.load(file)

    print("Preparing titles for filtering...")
    titles = [{"id": article["id"], "title": article["title"]} for article in articles]

    print("Defining and invoking filter chain...")
    filterPrompt = ChatPromptTemplate.from_messages([
        ("system", "Filter this list to only include entries which could have any geopolitical impact on the price of oil."),
        ("user", "{filterInput}" + "output in original json format.")
    ])
    filterChain = filterPrompt | llm | output_parser
    filterOut = filterChain.invoke({"filterInput": json.dumps(titles)})
    filteredList = json.loads(filterOut)

print("Updating filtered articles with summaries...")
summarisedInput = update_json_with_summaries(filteredArticles)

    print("Updating filtered articles with summaries...")
    update_json_with_summaries(filteredArticles)

print("Invoking sentiment analysis chain with filtered and summarized articles...")
output = chain.invoke({"input": json.dumps(summarisedInput)})

    print("Invoking sentiment analysis chain with filtered and summarized articles...")
    output = chain.invoke({"input": json.dumps(filteredArticles)})

    print("Final output:")
    print(output)
