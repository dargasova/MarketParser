# scrape_xpaths.py
# coding=utf-8

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from common_web_actions import close_cookies_banner
from page_navigation import scroll_page_down, go_to_next_page
import time

logging.basicConfig(
    filename='selenium_script.log',
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

URL = "https://www.wildberries.ru/catalog/elektronika/tv-audio-foto-video-tehnika/televizory/televizory"
MAX_ITEMS = 110
WAIT_TIME = 5


def scrape_xpaths():
    driver = webdriver.Firefox()
    driver.get(URL)
    driver.implicitly_wait(10)

    close_cookies_banner(driver)

    try:
        with open('xpaths.txt', 'w') as file:
            i = 1
            retries = 0
            total_items = 0
            page_number = 1

            while total_items < MAX_ITEMS:
                try:
                    xpath = f'/html/body/div[1]/main/div[2]/div/div[2]/div/div[4]/div[1]/div/div/article[{i}]/div/a'

                    driver.find_element(By.XPATH, xpath)

                    file.write(f"{xpath},{page_number}\n")

                    logging.info(f"Найден элемент с индексом {i} на странице {page_number}")

                    i += 1
                    retries = 0
                    total_items += 1

                    scroll_page_down(driver, i)

                except NoSuchElementException:
                    logging.warning(f"Элемент с индексом {i} не найден на странице {page_number}")

                    if retries < 2:
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                        time.sleep(WAIT_TIME)
                        retries += 1

                    else:
                        try:
                            logging.info(
                                f"Все элементы на странице {page_number} обработаны. Переходим на следующую страницу!")

                            try:
                                go_to_next_page(driver)

                                i = 1
                                retries = 0
                                page_number += 1

                            except NoSuchElementException:
                                logging.warning("Кнопка 'Следующая страница' не найдена или достигнут конец страниц")
                                break

                        except Exception as e:
                            logging.error(f"Ошибка при попытке перейти на следующую страницу: {e}")
                            break

        if total_items >= MAX_ITEMS:
            logging.info(f"Парсинг завершен успешно. Найдено {MAX_ITEMS} элементов!")
        else:
            logging.info("Парсинг завершен. Достигнут конец страниц или произошла ошибка")

    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_xpaths()
