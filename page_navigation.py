# page_navigation.py
# coding=utf-8

import logging
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

WAIT_TIME = 5


def go_to_next_page(driver):
    next_button = WebDriverWait(driver, WAIT_TIME).until(
        ec.element_to_be_clickable((By.LINK_TEXT, 'Следующая страница'))
    )
    next_button.click()
    logging.info("Клик на кнопку 'Следующая страница' выполнен!")
    time.sleep(WAIT_TIME)


def scroll_page_down(driver, element_count):
    if element_count % 20 == 0:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(WAIT_TIME)
