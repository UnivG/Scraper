import requests
from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import time
from multiprocessing import Process

def scrape_products_from_page(url, category):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_cards = soup.find_all(class_='card thumbnail')

    products_data = []

    for card in product_cards:
        name = card.find(class_='title').get('title')
        price = card.find(class_='price').text.strip()
        description = card.find(class_='description').text.strip()
        review_count = card.find(class_='review-count').text.strip()
        
        rating_element = card.find('p', {'data-rating': True})
        rating = rating_element['data-rating'] if rating_element else None

        products_data.append({
            'name': name,
            'price': price,
            'description': description,
            'review_count': review_count,
            'rating': rating,
            'category': category  
        })

    return products_data

def scrape_category(category_url, category_name):
    products_data = []

    page_number = 1
    while True:
        url = f"{category_url}?page={page_number}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        product_cards = soup.find_all(class_='card thumbnail')

        if not product_cards:
            break

        products_data.extend(scrape_products_from_page(url, category_name))
        page_number += 1

    uri = "mongodb+srv://kacper:test@baza1.flvotty.mongodb.net/?retryWrites=true&w=majority&appName=Baza1"
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client['products']
    collection = db['ecommerce']
    collection.delete_many({'category': category_name})

    result = collection.insert_many(products_data)
    print(f"{len(result.inserted_ids)} products inserted for category: {category_name}")

if __name__ == '__main__':
    categories = [
        ("https://webscraper.io/test-sites/e-commerce/static/computers/laptops", "computers"),
        ("https://webscraper.io/test-sites/e-commerce/static/phones/touch", "phones")
    ]

    processes = []

    for category_url, category_name in categories:
        process = Process(target=scrape_category, args=(category_url, category_name))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
