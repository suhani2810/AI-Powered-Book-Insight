from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import time
from openai import OpenAI
import json

BASE_URL = "http://127.0.0.1:8000/books/"

try:
    response = requests.get(BASE_URL)
    response.raise_for_status()
    existing_books = response.json()
except Exception as e:
    print("API not reachable:", e)
    existing_books = []

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def generate_ai_insights(title, description):
    prompt = f"""
    Book Title: {title}
    Description: {description}

    Return ONLY JSON:
    {{
        "summary": "2-3 line summary",
        "genre": "single genre"
    }}
    """

    response = client.chat.completions.create(
        model="mistral-7b-instruct-v0.1:2",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return json.loads(response.choices[0].message.content)


response = requests.get(BASE_URL)

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)

existing_books = response.json()
existing_titles = {book["title"]: book for book in existing_books}


service = Service(r"C:\Users\KIIT\ai_book_project\chromedriver.exe")
driver = webdriver.Chrome(service=service)


def scrape_page(url):
    driver.get(url)
    time.sleep(2)

    books = driver.find_elements(By.CLASS_NAME, "product_pod")

    for book in books:
        try:
            title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
            price = book.find_element(By.CLASS_NAME, "price_color").text
            rating = book.find_element(By.CLASS_NAME, "star-rating").get_attribute("class").split()[-1]
            link = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("href")

            description = f"A book titled {title} priced at {price}"

            existing_book = existing_titles.get(title)

            if existing_book and existing_book.get("summary") and existing_book.get("genre"):
                print("Skipping:", title)
                continue

            try:
                ai_output = generate_ai_insights(title, description)
            except Exception as e:
                print("AI failed:", e)
                ai_output = {
                    "summary": "No summary available",
                    "genre": "Unknown"
                }

            payload = {
                "title": title,
                "price": price,
                "rating": rating,
                "link": link,
                "description": description,
                "summary": ai_output["summary"],
                "genre": ai_output["genre"]
            }

            if existing_book:
                response = requests.put(f"{BASE_URL}{existing_book['id']}/", json=payload)
                print("Updated:", title, response.status_code)
            else:
                response = requests.post(BASE_URL, json=payload)
                print("Created:", title, response.status_code)

                if response.status_code == 201:
                    existing_titles[title] = response.json()

            time.sleep(1)

        except Exception as e:
            print("Error scraping book:", e)

for page in range(1, 6):
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    print(f"\nScraping Page {page}...")
    scrape_page(url)

driver.quit()