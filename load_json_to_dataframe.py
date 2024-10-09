# load_json_to_dataframe.py
# coding=utf-8

import pandas as pd
import json
from prettytable import PrettyTable


def load_json_to_dataframe(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame.from_dict(data, orient='index')

    return df


def get_normalized_brands(df):
    if 'Бренд' not in df.columns:
        raise ValueError("Столбец 'Бренд' отсутствует в DataFrame")

    most_common_brand = df['Бренд'].mode()[0] if not df['Бренд'].mode().empty else None

    df['Бренд'] = df['Бренд'].fillna(most_common_brand)

    normalized_brands = df['Бренд'].drop_duplicates().str.title().tolist()

    return normalized_brands


def filter_above_average_price(df):
    if 'Финальная цена' not in df.columns:
        raise ValueError("Столбец 'Финальная цена' отсутствует в DataFrame")

    df['Финальная цена'] = pd.to_numeric(df['Финальная цена'], errors='coerce')

    average_price = df['Финальная цена'].mean()

    df_filtered = df.loc[df['Финальная цена'] > average_price]

    return df_filtered, average_price


def apply_discount_mask(df):
    if 'Старая цена' not in df.columns or 'Финальная цена' not in df.columns:
        raise ValueError("Отсутствуют столбцы 'Старая цена' или 'Финальная цена' в DataFrame")

    df['Старая цена'] = pd.to_numeric(df['Старая цена'], errors='coerce')
    df['Финальная цена'] = pd.to_numeric(df['Финальная цена'], errors='coerce')

    discount_mask = df['Старая цена'] > df['Финальная цена']

    df_discounted = df.loc[discount_mask]

    return df_discounted


def combine_name_and_price(df):
    if 'Название' not in df.columns or 'Финальная цена' not in df.columns:
        raise ValueError("Отсутствуют столбцы 'Название' или 'Финальная цена' в DataFrame.")

    df_valid = df.dropna(subset=['Название', 'Финальная цена']).copy()

    df_valid['Название и цена'] = df_valid['Название'] + ' - ' + df_valid['Финальная цена'].astype(str)

    return df_valid[['Название и цена']]


def display_table(title, data_frame):
    table = PrettyTable()
    table.title = title
    table.field_names = ['Страница'] + data_frame.columns.tolist()

    for _ in table.field_names:
        table.align[_] = 'l'

    for index, row in data_frame.iterrows():
        table.add_row([index] + row.tolist())

    print(table)


def process_wildberries_data(file_path):
    df = load_json_to_dataframe(file_path)

    normalized_brands = get_normalized_brands(df)
    print("Уникальные бренды:")
    print(", ".join(normalized_brands))

    df_above_average_price, average_price = filter_above_average_price(df)
    print(f"\nСредняя цена: {average_price:.}")
    print("\nТовары с ценой выше средней:")
    display_table("Товары с ценой выше средней", df_above_average_price[['Название', 'Финальная цена']])

    df_discounted = apply_discount_mask(df)
    print("\nТовары со скидкой:")
    display_table("Товары со скидкой", df_discounted[['Название', 'Финальная цена', 'Старая цена']])

    df_combined = combine_name_and_price(df)
    print("\nОбъединённые названия и цены:")
    display_table("Объединённые названия и цены", df_combined)


process_wildberries_data('pages_data.json')
