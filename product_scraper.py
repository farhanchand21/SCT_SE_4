import requests
from bs4 import BeautifulSoup
import csv

# Convert rating words to numbers
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# CSV file setup
csv_file = open("products.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(["Product Name", "Price (£)", "Rating"])

# Loop through pages 1–5 (can increase)
for page in range(1, 6):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Select all product cards
    products = soup.select("article.product_pod")

    for product in products:

        # Extract Name
        name = product.h3.a["title"]

        # Extract Price
        price = product.select_one(".price_color").get_text(strip=True)
        price = price.replace("£", "")  # Clean currency symbol

        # Extract Rating
        rating_class = product.select_one("p.star-rating")["class"][1]
        rating = rating_map.get(rating_class, "N/A")

        # Save to CSV
        writer.writerow([name, price, rating])

    print(f"Page {page} scraped successfully.")

csv_file.close()
print("\n✅ Scraping complete! Data saved into products.csv")
