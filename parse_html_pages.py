# parse_html_pages.py
# coding=utf-8


import os
import logging
import json
from lxml import html

from extractors import (
    get_name, get_article, get_wallet_price, get_delivery_date,
    get_seller, get_product_rating, get_reviews_count, get_price_change,
    get_seller_rating, get_model, get_os, get_specs, get_brand, get_final_price, get_old_price
)

SAVE_DIR = 'saved_pages'

logging.basicConfig(
    filename='selenium_script.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_html_page(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        tree = html.fromstring(content)
        logging.info(f"HTML-страница {file_path} успешно загружена и преобразована в дерево lxml.")
        return tree
    except FileNotFoundError:
        logging.error(f"Файл {file_path} не найден.")
    except Exception as e:
        logging.error(f"Ошибка при загрузке файла {file_path}: {e}")
    return None


def process_saved_pages():
    if not os.path.exists(SAVE_DIR):
        logging.error(f"Директория {SAVE_DIR} не найдена.")
        return

    logging.info(f"Начинается обработка страниц в директории {SAVE_DIR}.")
    result = {}

    for root, dirs, files in os.walk(SAVE_DIR):
        dirs.sort(key=lambda x: int(x.split('_')[1]))

        for dir_name in dirs:
            dir_path = os.path.join(SAVE_DIR, dir_name)

            html_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.html')],
                                key=lambda x: int(x.split('_')[1].split('.')[0]))

            for file in html_files:
                file_path = os.path.join(dir_path, file)
                tree = load_html_page(file_path)

                if tree is not None:
                    page_data = {
                        "Название": get_name(tree),
                        "Артикул": get_article(tree),
                        "Бренд": get_brand(tree),
                        "Модель": get_model(tree),
                        "Операционная система": get_os(tree),
                        "Рейтинг товара": get_product_rating(tree),
                        "Количество оценок": get_reviews_count(tree),
                        "Цена с WB кошельком": get_wallet_price(tree),
                        "Финальная цена": get_final_price(tree),
                        "Старая цена": get_old_price(tree),
                        "Изменение цены": get_price_change(tree),
                        "Дата доставки": get_delivery_date(tree),
                        "Продавец": get_seller(tree),
                        "Рейтинг продавца": get_seller_rating(tree),

                    }

                    specs = get_specs(tree)
                    if specs:
                        page_data.update(specs)

                    result[file] = page_data

    with open('pages_data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    logging.info("Обработка всех страниц завершена.")


if __name__ == "__main__":
    process_saved_pages()
