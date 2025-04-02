import csv
import time
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--ignore-certificate-errors")

    return webdriver.Chrome(options=chrome_options)

def parse_product(product):
    try:
        name = product.find_element(By.CSS_SELECTOR, "div.Product_model__2lQkH").text.strip()
        price = product.find_element(By.CSS_SELECTOR, "div.ProductPrice_price__KP1kd").text.strip().replace("₽", "").replace(" ", "")
        link = product.find_element(By.CSS_SELECTOR, "a.Product_link__SS3rL").get_attribute("href")
        product_type = product.find_element(By.CSS_SELECTOR, "div.Product_type__7uFnL").text.strip()

        try:
            rating = product.find_element(By.CSS_SELECTOR, "div.ProductReview_rating__mU5DT").text.strip()
            reviews = product.find_element(By.CSS_SELECTOR, "div.ProductReview_count___Jebz").text.strip()
        except:
            rating = "No rating"
            reviews = "0"

        return {
            "Name": name,
            "Type": product_type,
            "Price": price,
            "Rating": rating,
            "Reviews": reviews,
            "Link": link
        }

    except Exception as e:
        try:
            bunner = product.find_element(By.CSS_SELECTOR, "div.Banner_banner__Uyok9")
            print("Found bunner")
            return None
        except:
            print(f"Error when parsing: {e}")
            return None
        
def next_page(driver):
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-listing-pagination='next']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
        next_btn.click()
        return True
    
    except:
        return False


def parse_page(driver, url, max_items):
    driver.get(url)
    time.sleep(2)
    
    try:
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.js-cookie-data-warning__close"))
        )
        cookie_btn.click()
    except:
        pass
    
    items = []
    page_num = 1
    
    while len(items) < max_items:
        print(f"Page parsing: {page_num}...")

        products = driver.find_elements(By.CSS_SELECTOR, "div.ProductGrid_gridItem__5rrh7")
        for product in products:

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)
            product_data = parse_product(product)

            if product_data:
                is_duplicate = any(
                    item["Link"] == product_data["Link"]
                    for item in items
                )
                if not is_duplicate:
                    items.append(product_data)
                    print(f"Added: {product_data["Name"]}")

            if len(items) >= max_items:
                return items
            
        if next_page(driver):
            time.sleep(2)
            page_num += 1
        else:
            print("It is all")
            break
    
    return items

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Name", "Type", "Price", "Rating", "Reviews", "Link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Successfully saved {len(data)} items to file {filename}")

def main():
    parser = argparse.ArgumentParser(description='Askona product parser')
    parser.add_argument('url', type=str, help='URL of Askona catalog page')
    parser.add_argument('--count', type=int, default=5, help='Number of items to be parsed')
    parser.add_argument('--output', type=str, default='askona_products.csv', help='CSV output file name')
    args = parser.parse_args()
    
    driver = create_driver()
    try:
        products = parse_page(driver, args.url, args.count)
        save_to_csv(products, args.output)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()