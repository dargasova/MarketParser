# common_web_actions.py
# coding=utf-8

import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

WAIT_TIME = 5


def close_cookies_banner(driver):
    try:
        cookie_button = WebDriverWait(driver, WAIT_TIME).until(
            ec.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/button'))
        )
        cookie_button.click()
        logging.info("Баннер с cookies закрыт!")
    except TimeoutException:
        logging.error("Не удалось найти кнопку 'Окей' для закрытия баннера с cookies")
    except NoSuchElementException:
        logging.error("Кнопка 'Окей' для закрытия баннера с cookies не найдена")
    except Exception as e:
        logging.error(f"Ошибка при закрытии баннера с cookies: {e}")


def find_element_with_retries(driver, xpath, retries=2):
    for attempt in range(retries + 1):
        try:
            return driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            if attempt < retries:
                logging.warning(f"Попытка {attempt + 1}: Элемент с XPATH {xpath} не найден, повторная попытка...")
                time.sleep(WAIT_TIME)
            else:
                logging.error(f"Элемент с XPATH {xpath} не найден после {retries + 1} попыток.")
                return None


def wait_for_page_load(driver):
    try:
        # Ожидание полной загрузки всех изображений на странице
        WebDriverWait(driver, 20).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )
        logging.info("Все изображения на странице загружены!")

        logging.info("Все карточки товаров загружены!")

    except TimeoutException:
        logging.error("Ошибка: время ожидания загрузки страницы истекло")
