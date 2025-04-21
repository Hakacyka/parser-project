import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Указываем путь к chromedriver
chrome_driver_path = "C:/Users/user/parser/chromedriver.exe"

# Настройки браузера
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# Запуск драйвера
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

url = "https://lux-texcv.com.ua/ru/kataloh/postelnoe-belie/"
driver.get(url)
time.sleep(3)

products = driver.find_elements(By.CSS_SELECTOR, "li.product")

print(f"Найдено товаров: {len(products)}")

data = []

for product in products:
    try:
        full_title = product.find_element(By.CSS_SELECTOR, "h2.woocommerce-loop-product__title").text.strip()
        link = product.find_element(By.TAG_NAME, "a").get_attribute("href").strip()
        price = product.find_element(By.CSS_SELECTOR, "span.woocommerce-Price-amount").text.strip()

        # Ищем артикул в конце названия (например, K5813)
        match = re.search(r'^(.*)\s+(K\d+)$', full_title)
        if match:
            title = match.group(1).strip()
            sku = match.group(2).strip()
        else:
            title = full_title
            # Если артикул не найден в названии — пробуем взять из DOM
            try:
                sku_elem = product.find_element(By.CSS_SELECTOR, "div.product-sku")
                sku = sku_elem.text.strip()
            except:
                sku = "—"

        data.append([title, link, price, sku])

    except Exception as e:
        print(f"Ошибка при обработке товара: {e}")

driver.quit()

# Сохраняем CSV с правильной кодировкой и заголовками
with open("tovary.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file, delimiter=";", quoting=csv.QUOTE_ALL)
    writer.writerow(["Название", "Ссылка", "Цена", "Артикул"])
    writer.writerows(data)

print(f"Сохранено товаров: {len(data)} в 'tovary.csv'")
