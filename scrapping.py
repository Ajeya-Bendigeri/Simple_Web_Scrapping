import requests
from bs4 import BeautifulSoup
import pandas as pd

current_page = 1

proceed = True

book_data = []

while(proceed):
    print("Current Scrapping Page No:" + str(current_page))
    url = "https://books.toscrape.com/catalogue/page-" + str(current_page) + ".html"

    data = requests.get(url)

    soup = BeautifulSoup(data.text, "html.parser")

    if soup.title.text == "404 Not Found":
        proceed = False
    else:
        all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for book in all_books:
            item = {}

            item['Title'] = book.find('img').attrs["alt"]
            item['Link'] = book.find('a').attrs["href"]
            item['Price'] = book.find('p', class_="price_color").text[2:]
            item['Stock'] = book.find('p', class_="instock availability").text.strip()

            book_data.append(item)

    current_page += 1

# Save the data into a CSV file
df = pd.DataFrame(book_data)
df.to_csv("book_data.csv", index=False)