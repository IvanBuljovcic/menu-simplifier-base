import argparse
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

def scrape_ingredients(url):
    # Set up Selenium WebDriver with headless Edge
    edge_options = Options()
    edge_options.add_argument("--headless")  # Run in headless mode (no browser UI)
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to msedgedriver.exe in the same directory as the script
    driver_path = os.path.join(script_dir, "msedgedriver.exe")
    # Set up the Service using the dynamically constructed path
    service = Service(driver_path)

    driver = webdriver.Edge(service=service, options=edge_options)
    driver.get(url)

    # Wait for the page to load and elements to be rendered
    # driver.implicitly_wait(2)

    # Find all elements with data-test-id="horizontal-item-card"
    cards = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="horizontal-item-card"]')

    print(f"Found {len(cards)} cards")

    items = []
    for index, card in enumerate(cards, start=1):
        try:
            # Extract the name/title
            try:
                title_element = card.find_element(By.CSS_SELECTOR, '[data-test-id="horizontal-item-card-header"]')
                name = title_element.text.strip() if title_element else "Unknown"
            except Exception:
                name = "Unknown"
                print(f"Card {index}: Failed to retrieve name.")

            # Extract the price
            try:
                price_element = card.find_element(By.CSS_SELECTOR, '[data-test-id="horizontal-item-card-price"]')
            except Exception:
                price_element = card.find_element(By.CSS_SELECTOR, '[data-test-id="horizontal-item-card-discounted-price"]')

            price = price_element.text.strip() if price_element else "Unknown"

            # Extract the ingredients
            try:
                ingredients_element = card.find_element(By.CSS_SELECTOR, '[data-test-id="horizontal-item-card-header"] + p')
                ingredients = [item.strip() for item in ingredients_element.text.split(",")] if ingredients_element else []
            except Exception:
                ingredients = []
                print(f"Card {index}: Failed to retrieve ingredients.")

            # Append the structured data
            items.append({
                "name": name,
                "ingredients": ingredients,
                "price": price
            })

        except Exception as e:
            print(f"Card {index}: Error processing card: {e}")

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

# Main function to parse arguments and run the scraper
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape menu data from a URL.")
    parser.add_argument("url", help="The URL of the restaurant page to scrape")
    args = parser.parse_args()

    # Use the URL provided as a command-line argument
    try:
        items_list = scrape_ingredients(args.url)

        # Define the data folder path and the file path
        data_folder = os.path.join(os.path.dirname(__file__), 'data')
        file_path = os.path.join(data_folder, 'menu.json')
        
        # Create the 'data' folder if it does not exist
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
            
        # Save the menu data to the menu.json file inside the 'data' folder
        with open(file_path, 'w') as json_file:
            json.dump(items_list, json_file, indent=4)

        # save_to_json(ingredients_list, "data/menu.json")
    except Exception as e:
        print(f"An error occurred while scraping: {e}")
