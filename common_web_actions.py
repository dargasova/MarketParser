# common_web_actions.py
# coding=windows-1251

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
        logging.info("������ � cookies ������!")
    except TimeoutException:
        logging.error("�� ������� ����� ������ '����' ��� �������� ������� � cookies")
    except NoSuchElementException:
        logging.error("������ '����' ��� �������� ������� � cookies �� �������")
    except Exception as e:
        logging.error(f"������ ��� �������� ������� � cookies: {e}")


def find_element_with_retries(driver, xpath, retries=2):
    for attempt in range(retries + 1):
        try:
            return driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            if attempt < retries:
                logging.warning(f"������� {attempt + 1}: ������� � XPATH {xpath} �� ������, ��������� �������...")
                time.sleep(WAIT_TIME)
            else:
                logging.error(f"������� � XPATH {xpath} �� ������ ����� {retries + 1} �������.")
                return None
