import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for the quotes website
base_url = "http://quotes.toscrape.com/page/{}/"

# Function to scrape a single page
def scrape_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    quotes = soup.find_all('div', class_='quote')
    
    page_quotes = []
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        page_quotes.append([text, author])
    
    return page_quotes

# List to store all quotes
all_quotes = []

# Loop through the first 5 pages
for page in range(1, 6):
    url = base_url.format(page)
    quotes_on_page = scrape_page(url)
    all_quotes.extend(quotes_on_page)

# Create a DataFrame and save to CSV
df = pd.DataFrame(all_quotes, columns=['Quote', 'Author'])
df.to_csv('quotes.csv', index=False)
print("Data saved to quotes.csv")
