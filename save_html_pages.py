# save_html_pages.py
# coding=windows-1251

import os
import shutil
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from common_web_actions import close_cookies_banner, find_element_with_retries
from page_navigation import scroll_page_down, go_to_next_page
import time

URL = "https://www.wildberries.ru/catalog/elektronika/tv-audio-foto-video-tehnika/televizory/televizory"
WAIT_TIME = 5
SAVE_DIR = 'saved_pages'

logging.basicConfig(
    filename='selenium_script.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def create_or_clear_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    logging.info(f"Директория {directory} создана или очищена!")


def save_element_html(driver, page_folder_name, element_index):
    os.makedirs(page_folder_name, exist_ok=True)
    page_source = driver.page_source
    file_name = f"page_{element_index}.html"
    with open(os.path.join(page_folder_name, file_name), 'w', encoding='utf-8') as file:
        file.write(page_source)
    logging.info(f"HTML-страница элемента сохранена в {page_folder_name}/{file_name}")


def process_xpaths():
    driver = webdriver.Firefox()
    driver.get(URL)
    driver.implicitly_wait(10)

    close_cookies_banner(driver)

    current_page_number = 1

    create_or_clear_dir(SAVE_DIR)

    try:
        with open('xpaths.txt', 'r') as file:
            lines = file.readlines()

            for index, line in enumerate(lines):
                xpath, page_number = line.strip().split(',')
                page_number = int(page_number)

                while page_number != current_page_number:
                    try:
                        logging.info(f"Переход на следующую страницу {current_page_number + 1}")

                        go_to_next_page(driver)

                        current_page_number += 1

                    except (NoSuchElementException, TimeoutException) as e:
                        logging.error(f"Ошибка при попытке перейти на следующую страницу: {e}")
                        driver.quit()
                        return

                page_folder_name = os.path.join(SAVE_DIR, f"page_{current_page_number}")

                scroll_page_down(driver, lines.index(line))

                elem = find_element_with_retries(driver, xpath)
                if elem:
                    elem.send_keys(Keys.RETURN)
                    logging.info(f"Открытие элемента по XPATH {xpath} на странице {page_number} выполнено!")
                    time.sleep(1)
                    save_element_html(driver, page_folder_name, index + 1)
                    driver.back()
                    time.sleep(1)

    except FileNotFoundError:
        logging.error("Файл xpaths.txt не найден")

    finally:
        driver.quit()
        logging.info("Обработка завершена!")


if __name__ == "__main__":
    process_xpaths()
