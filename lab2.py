import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

query = "rose"
num_images = 1000
folder = "dataset/rose"

os.makedirs(folder, exist_ok=True)

driver = webdriver.Chrome()
driver.get(f"https://yandex.ru/images/search?text={query}")
time.sleep(5)
scroll_count = 0


while scroll_count < num_images // 25:
    element = driver.find_element(By.TAG_NAME, 'body')
    element.send_keys(Keys.END)
    time.sleep(1)
    scroll_count += 1
    try:
        button = driver.find_element(By.CLASS_NAME, 'button2')
        button.click()
    except:
        pass

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

thumbnails = soup.find_all("img", class_="serp-item__thumb")
count = 0

for thumbnail in thumbnails[:num_images]:
    try:
        full_image_url = thumbnail["src"]

        filename = f"{str(count).zfill(4)}.jpg"
        urlretrieve("https:" + full_image_url, os.path.join(folder, filename))

        count += 1

        if count >= num_images:
            break
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")

driver.quit()
