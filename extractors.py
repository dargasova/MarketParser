# extractors.py
# coding=utf-8

import logging
import re


def get_name(tree):
    try:
        return tree.xpath('//h1[contains(@class, "product-page__title")]/text()')[0].strip()
    except IndexError:
        logging.warning("Название не найдено.")
        return None


def get_article(tree):
    try:
        return tree.xpath('//*[@id="productNmId"]/text()')[0].strip()
    except IndexError:
        logging.warning("Артикул не найден.")
        return None


def get_brand(tree):
    try:
        return tree.xpath('//a[contains(@class, "product-page__header-brand")]/text()')[0].strip()
    except IndexError:
        logging.warning("Бренд не найден.")
        return None


def get_model(tree):
    try:
        return tree.xpath('//td[@class="product-params__cell"]/span/text()')[0].strip()
    except IndexError:
        logging.warning("Модель не найдена.")
        return None


def get_os(tree):
    try:
        return tree.xpath('(//td[@class="product-params__cell"]/span/text())[2]')[0].strip()

    except IndexError:
        logging.warning("Операционная система не найдена.")
        return None


def get_specs(tree):
    try:
        specs_text = tree.xpath('//div[contains(@class, "glued-options")]/p/text()')[0].strip()

        matches = re.findall(r'(\d+)\" • ([^,]+)', specs_text)

        specs_dict = {}
        for diagonal, color in matches:
            specs_dict["Диагональ"] = diagonal.strip()
            specs_dict["Цвет"] = color.strip()

        return specs_dict

    except IndexError:
        logging.warning("Характеристики не найдены.")
        return None


def get_product_rating(tree):
    try:
        return tree.xpath('//span[contains(@class, "product-review__rating")]/text()')[0].strip()
    except IndexError:
        logging.warning("Рейтинг товара не найден.")
        return None


def get_reviews_count(tree):
    try:
        return tree.xpath('//span[contains(@class, "product-review__count-review")]/text()')[0].strip()
    except IndexError:
        logging.warning("Количество оценок не найдено.")
        return None


def get_wallet_price(tree):
    try:
        price = tree.xpath('//span[contains(@class, "price-block__wallet-price")]/text()')[0].strip()
        return clean_price(price)
    except IndexError:
        logging.warning("Цена с WB кошельком не найдена.")
        return None


def get_final_price(tree):
    try:
        final_price = tree.xpath('//ins[contains(@class, "price-block__final-price")]/text()')[0].strip()
        return clean_price(final_price)
    except IndexError:
        logging.warning("Финальная цена не найдена.")
        return None


def get_old_price(tree):
    try:
        old_price = tree.xpath('//del[contains(@class, "price-block__old-price")]/span/text()')[0].strip()
        return clean_price(old_price)
    except IndexError:
        logging.warning("Старая цена не найдена.")
        return None


def get_price_change(tree):
    try:
        price_change = tree.xpath('//span[contains(@class, "price-history__trend")]/text()')[0].strip()
        return clean_price(price_change)
    except IndexError:
        logging.info("Цена не изменялась")
        return "Цена не изменялась"


def clean_price(price_string):
    cleaned_price = re.sub(r'\D', '', price_string)
    return cleaned_price


def get_delivery_date(tree):
    try:
        return tree.xpath('normalize-space(//div[contains(@class, "delivery__title")])').strip()
    except IndexError:
        logging.warning("Дата доставки не найдена.")
        return None


def get_seller(tree):
    try:
        return tree.xpath('//span[contains(@class, "seller-info__name")]/text()')[0].strip()
    except IndexError:
        logging.warning("Продавец не найден.")
        return None


def get_seller_rating(tree):
    try:

        return tree.xpath('//div[@class="seller-info__param"]//span[contains(@class, "address-rate-mini")]/text()')[
            0].strip()

    except IndexError:
        logging.warning("Рейтинг продавца не найден.")
        return None
