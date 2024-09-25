# common_web_actions.py
# coding=utf-8

import logging

from selenium.webdriver import Keys
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


def scroll_page_down(driver, times=1):
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(times):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)


def scroll_page_up(driver):
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.HOME)
    time.sleep(1)


def wait_for_page_load(driver):
    try:
        scroll_page_down(driver, 2)

        WebDriverWait(driver, 20).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )
        logging.info("Все изображения на странице загружены!")

        scroll_page_up(driver)

    except TimeoutException:
        logging.error("Ошибка: время ожидания загрузки страницы истекло")
