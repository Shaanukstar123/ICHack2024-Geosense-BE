import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from summariser.summariser import summarise_text

def update_json_with_summaries(articles):
    print("Starting summarization...")
    count = 0
    summaries = []
    for article in articles:
        if count >= 5:
            break
        try:
            print(f"Summarizing article ID: {article['id']}")
            summary = summarise_text(article['content'])
            article['content'] = summary
            print(f"Summary for article ID: {article['id']} completed")
            summaries.append(article)
            count += 1
        except Exception as e:
            print(f"Error summarizing article ID: {article['id']}: {e}")
            article['content'] = "Summary unavailable"
    return summaries

def analyse():
    print("Initializing Langchain components...")
    llm = ChatOpenAI(openai_api_key=os.environ.get("OPEN_API_KEY"), model="gpt-4")
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

    print("Compiling a list of filtered articles...")
    filteredIndexes = [int(article["id"]) for article in filteredList]
    filteredArticles = [article for article in articles if article["id"] in filteredIndexes]
    print(f"Number of articles after filtering: {len(filteredArticles)}")

    print("Updating filtered articles with summaries...")
    summarisedInput = update_json_with_summaries(filteredArticles)

    print("Defining sentiment analysis prompt and chain...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Give me geopolitical sentiment indexes to 3 decimal places ranging from -1 to 1 continuous values for a financial analyst interested in oil. Also provide a short reason justifying the sentiment value."),
        ("system", "Give me the two letter country codes of the country that each sentiment is referring to. Provide the output in JSON form id: , countries: [], sentiment indexes: [], reason: "),
        ("user", "{input}")
    ])
    chain = prompt | llm | output_parser

    print("Invoking sentiment analysis chain with filtered and summarized articles...")
    output = json.loads(chain.invoke({"input": json.dumps(summarisedInput)}))

    print("2nd Final output:")
    print(output)

    final_output = {}
    for item in output:
        # Iterate over each country in the countries list
        for i, country_code in enumerate(item["countries"]):
            # Use the country code as the key
            # Extract the sentiment index and reason, and assign them to the country code key
            final_output[country_code.lower()] = {
                "value": item["sentiment_indexes"][i],
                "message": item["reason"]
            }

    print("2nd Final output:")
    print(final_output)

    with open('finalOutput.json', 'w') as f:
        json.dump(final_output, f)

analyse()
