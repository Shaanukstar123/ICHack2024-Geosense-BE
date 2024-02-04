import requests
import pandas as pd
from datetime import datetime
from webCrawler.forbesScraper import run_spider
from newsAnalysis import analyse
import json

run_spider()
try:
    analyse()
except:
    pass



with open('finalOutput.json', 'r') as file:
    data = json.load(file)
# Data structure to upload
# data = {
#     "ca": {"value": 0, "message": "Canada is a country in North America. Its ten provinces and three territories extend from the Atlantic to the Pacific and northward into the Arctic Ocean, covering 9.98 million square kilometers, making it the world's second-largest country by total area."},
#     "cn": {"value": 1, "message": "China is a country in East Asia. It is the world's most populous country, with a population of over 1.4 billion."},
#     "id": {"value": -1, "message": "Indonesia is a country in Southeast Asia, between the Indian and Pacific oceans. It is the world's largest island country, with more than seventeen thousand islands."}
# }

# Convert to DataFrame
data_df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index': 'country'})
# data_df['country'] = datetime.utcnow().isoformat()  # Add a 'date' field with the current time

# Convert to JSON
json_data = data_df.to_json(orient='records')

# Your Firebase database URL (replace with your actual database URL)
firebase_url = "https://geosense-ai-default-rtdb.europe-west1.firebasedatabase.app/regions.json"

# Make an HTTP PUT request to upload the data
response = requests.put(firebase_url, data=json_data)

# Check the response
if response.ok:
    print("Data uploaded successfully")
else:
    print(f"Failed to upload data: {response.status_code}, {response.reason}")
