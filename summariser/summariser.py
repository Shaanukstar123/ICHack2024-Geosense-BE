import requests
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def summarise_text(input_text, min_length=20, max_length=50, language="auto"):
    url = "https://portal.ayfie.com/api/summarize"
    headers = {
        "X-API-KEY": "OuopxAaSscCaWBhKxtCdinmGbXHjJnMffkmAVgYjCotghIkYlg",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "language": language,
        "text": input_text,
        "min_length": min_length,
        "max_length": max_length
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['result']
    else:
        return response.json()

def update_json_with_summaries(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        articles = json.load(file)

    futures = []
    with ThreadPoolExecutor(max_workers=3) as executor: #threading agents
        for article in articles:
            futures.append(executor.submit(summarise_text, article['content']))

        for future, article in zip(as_completed(futures), articles):
            article['summary'] = future.result()

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(articles, file, indent=4, ensure_ascii=False)

# json_file = 'output.json' 
# update_json_with_summaries(json_file)

# {"2 character country string": [float -1 to 1, summary],

# }
# {
# value: average value
# datetime: date time right now
# }