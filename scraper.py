from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import json
import os

# URL of the target website
URL = "https://wolt.com/en/srb/belgrade/restaurant/smash-burgerss"

def scrape_ingredients(url):
    # Set up Selenium WebDriver with headless Edge
    edge_options = Options()
    edge_options.add_argument("--headless")  # Run in headless mode (no browser UI)
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    
    # Specify the full path to msedgedriver.exe
    service = Service(r"C:\Projects\Private\next-shadcn\msedgedriver.exe")  # Use the full path here

    driver = webdriver.Edge(service=service, options=edge_options)
    driver.get(url)

    # Wait for the page to load and elements to be rendered
    driver.implicitly_wait(10)

    # Find all elements with data-test-id="horizontal-item-card"
    cards = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="horizontal-item-card"]')

    print(f"Found {len(cards)} cards")

    items = []
    for card in cards:
        try:
            # Extract the name/title from the element with data-test-id="horizontal-item-card-header"
            title_element = card.find_element(By.CSS_SELECTOR, '[data-test-id="horizontal-item-card-header"]')
            name = title_element.text.strip() if title_element else "Unknown"

            # Extract the price from the element with data-test-id="horizontal-item-card-price"
            price_element = card.find_element(By.CSS_SELECTOR, '[data-test-id="horizontal-item-card-price"]')
            price = price_element.text.strip() if price_element else "Unknown"

            # Extract the ingredients from the <p> tag adjacent to .horizontal-item-card-header
            ingredients_element = card.find_element(By.CSS_SELECTOR, '[data-test-id="horizontal-item-card-header"] + p')
            ingredients = [item.strip() for item in ingredients_element.text.split(",")] if ingredients_element else []

            # Append the structured data to the items list
            items.append({
                "name": name,
                "ingredients": ingredients,
                "price": price
            })

        except Exception as e:
            print(f"Error processing card: {e}")
    
    # Quit the browser
    driver.quit()

    return items

def save_to_json(data, filename):
    # Save data to a JSON file in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Data saved to {filepath}")

# Scrape the ingredients and save them to a JSON file
if __name__ == "__main__":
    ingredients_list = scrape_ingredients(URL)
    save_to_json(ingredients_list, "ingredients.json")
