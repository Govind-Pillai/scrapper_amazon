import requests
from bs4 import BeautifulSoup
import csv

def scrape_products(url, filename):
  """Scrapes product details from Amazon and saves them to a CSV file."""
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}  # Mimic a browser to avoid blocking
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'lxml')

  products = []
  for product in soup.find_all('div', class_='s-product-grid__item'):
    try:
      name_element = product.find('span', class_='a-size-medium a-color-base a-text-normal')
      name = name_element.text.strip()

      price_element = product.find('span', class_='a-offscreen')
      price = price_element.text.strip() if price_element else 'Not Available'

      rating_element = product.find('span', class_='a-icon-alt')
      rating = rating_element.text.strip() if rating_element else 'No Rating'

      seller_element = product.find('a', class_='a-size-small a-color-secondary')
      seller = seller_element.text.strip() if seller_element else 'N.A.'
    except:
      # Handle potential errors during scraping
      continue

    products.append({'name': name, 'price': price, 'rating': rating, 'seller': seller})

  # Write data to CSV file
  with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['name', 'price', 'rating', 'seller']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)

  print(f"Scraped {len(products)} products and saved to {filename}")

# Replace with the desired filename
filename = 'C:/Users/Govind/Python_Study/Webapp/amazon_products.csv'
url = 'https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar'

scrape_products(url, filename)
