import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AskonaParser:
    def __init__(self):
        self.driver = self.create_driver()
        self.max_items = 10

    def create_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--ignore-certificate-errors")
        return webdriver.Chrome(options=chrome_options)

    def parse_product(self, product):
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
                "name": name,
                "type": product_type,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "link": link
            }
        except Exception as e:
            try:
                banner = product.find_element(By.CSS_SELECTOR, "div.Banner_banner__Uyok9")
                print("Found banner")
                return None
            except:
                print(f"Error when parsing: {e}")
                return None

    def next_page(self):
        try:
            next_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-listing-pagination='next']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
            next_btn.click()
            return True
        except:
            return False

    def parse(self, url, max_items=None):
        if max_items is None:
            max_items = self.max_items

        self.driver.get(url)
        time.sleep(2)
        
        try:
            cookie_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.js-cookie-data-warning__close"))
            )
            cookie_btn.click()
        except:
            pass
        
        items = []
        page_num = 1
        
        while len(items) < max_items:
            print(f"Parsing page {page_num}...")
            products = self.driver.find_elements(By.CSS_SELECTOR, "div.ProductGrid_gridItem__5rrh7")
            
            for product in products:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)
                product_data = self.parse_product(product)
                
                if product_data and not any(item['link'] == product_data['link'] for item in items):
                    items.append(product_data)
                    print(f"Product added: {product_data['name']}")
                
                if len(items) >= max_items:
                    return items
            
            if not self.next_page():
                break
            time.sleep(2)
            page_num += 1
        
        return items

    def close(self):
        self.driver.quit()