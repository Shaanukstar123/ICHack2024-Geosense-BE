import requests
import pandas as pd

# Specify the URL for GDP data from the World Bank API
url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&date=2020&per_page=300"

# Make the HTTP request to the World Bank API
response = requests.get(url)
data = response.json()

# Parse the JSON data and extract relevant information
countries = [entry['country']['value'] for entry in data[1]]
gdps = [entry['value'] for entry in data[1]]

# Create a DataFrame with the extracted data
gdp_data = pd.DataFrame({
    'Country': countries,
    'GDP': gdps
})

# Handle missing values as needed, e.g., drop, fill, etc.
gdp_data.dropna(inplace=True)

# Save the DataFrame to a CSV file
gdp_data.to_csv('gdp_data.csv', index=False)

# print("GDP data saved to 'gdp_data.csv'")

# print(gdp_data)
sorted_df = gdp_data.sort_values(by='GDP', ascending=False)

non_countries = ['World', 'High income', 'OECD members', 'Post-demographic dividend', 'IDA & IBRD total', 'Low & middle income', 'Middle income', 'IBRD only']
sorted_df = sorted_df[~sorted_df['Country'].isin(non_countries)]
print(sorted_df)