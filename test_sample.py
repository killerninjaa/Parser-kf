from pandas.core.frame import DataFrame
import pytest
import json
from main import find_ch, find_mes, get_data, this_year, all_time, last_month, last_week, last_kvartal, main_s, get_page_soup, get_key, get_osobnyak_links, info
import unittest
from unittest import mock
from mock import patch
import pandas as pd

today_date = '2021-12-18'

def test_find_ch_z():
    """Тест проверяет корректность записи числа"""
    assert find_ch(7, 2) == '05' 

def test_find_ch_nz():
    """Тест проверяет корректность записи числа"""
    assert find_ch(13, 2) == '11'

def test_find_mes_z():
    """Тест проверяет корректность записи месяца"""
    assert find_mes(4, 3) == '01'

def test_find_mes_nz():
    """Тест проверяет корректность записи месяца"""
    assert find_mes(12, 1) == '11'

def test_get_data():
    """Тест проверяет корректность записи данных в текстовый файл"""
    with unittest.mock.patch(
        'main.main_s', 
        return_value=[
            {"Address": 'Особняк на Николоямской, 49с2',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2020-10-26", 
             "Square": "1108", 
             "Price": "60000000", 
             "Price per square meter": 54152},
             {"Address": 'Особняк на Александрова, 18',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2028-12-31", 
             "Square": "1678", 
             "Price": "87000000", 
             "Price per square meter": 98152}
             ]):
        flag = False
        get_data()
        ans = [
             {"Address": 'Особняк на Николоямской, 49с2',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2020-10-26", 
             "Square": "1108", 
             "Price": "60000000", 
             "Price per square meter": 54152},
             {"Address": 'Особняк на Александрова, 18',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2028-12-31", 
             "Square": "1678", 
             "Price": "87000000", 
             "Price per square meter": 98152}
             ]
        file = open("list_info.txt", 'r')
        list_info = json.load(file)
        assert list_info == ans

def test_all_time():
    """Тест проверяет корректность записи данных в эксель"""
    with unittest.mock.patch(
        'main.get_data',
         return_value=[
             {"Address": 'Особняк на Николоямской, 49с2',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2020-10-26", 
             "Square": "1108", 
             "Price": "60000000", 
             "Price per square meter": 54152},
             ]):
        all_time()
        ans = {"Address": {0: 'Особняк на Николоямской, 49с2'},
             "Link": {0: "https://osobnyaki.com//na-nikoloyamskoy-49s2"}, 
             "Date added": {0: "2020-10-26"}, 
             "Square": {0: 1108}, 
             "Price": {0: 60000000}, 
             "Price per square meter": {0: 54152}}
        df = pd.read_excel('info_excel_all.xlsx').to_dict()
        assert df == ans
    
def test_this_year():
    """Тест проверяет, что в эксель записываются данные только за нынешний год"""
    with unittest.mock.patch(
        'main.get_data',
         return_value=[
             {"Address": 'Особняк на Николоямской, 49с2',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2020-10-26", 
             "Square": "1108", 
             "Price": "60000000", 
             "Price per square meter": 54152},
             {"Address": 'Особняк на Александрова, 18',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2021-12-12", 
             "Square": "1788", 
             "Price": "60067867890", 
             "Price per square meter": 54152}
             ]):
        this_year(today_date)
        ans = {"Address": {0: 'Особняк на Александрова, 18'},
             "Link": {0: "https://osobnyaki.com//na-nikoloyamskoy-49s2"}, 
             "Date added": {0: "2021-12-12"}, 
             "Square": {0: 1788}, 
             "Price": {0: 60067867890}, 
             "Price per square meter": {0: 54152}} 
        df = pd.read_excel('info_excel_year.xlsx').to_dict()
        assert df == ans

def test_last_month():
    """Тест проверяет, что в эксель записываются данные только за прошлый месяц"""
    with unittest.mock.patch(
        'main.get_data',
         return_value=[
             {"Address": 'Особняк на Николоямской, 49с2',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2021-10-13", 
             "Square": "1108", 
             "Price": "60000000", 
             "Price per square meter": 54152},
             {"Address": 'Особняк на Александрова, 18',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2021-11-26", 
             "Square": "1788", 
             "Price": "60067867890", 
             "Price per square meter": 54152}
             ]):
        last_month(today_date)
        ans = {"Address": {0: 'Особняк на Александрова, 18'},
             "Link": {0: "https://osobnyaki.com//na-nikoloyamskoy-49s2"}, 
             "Date added": {0: "2021-11-26"}, 
             "Square": {0: 1788}, 
             "Price": {0: 60067867890}, 
             "Price per square meter": {0: 54152}} 
        df = pd.read_excel('info_excel_month.xlsx').to_dict()
        assert df == ans

def test_last_week():
    """Тест проверяет, что в эксель записываются данные только за прошедшие 7 дней"""
    with unittest.mock.patch(
        'main.get_data',
         return_value=[
             {"Address": 'Особняк на Николоямской, 49с2',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2021-12-18", 
             "Square": "1108", 
             "Price": "60000000", 
             "Price per square meter": 54152},
             {"Address": 'Особняк на Александрова, 18',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2021-12-16", 
             "Square": "1788", 
             "Price": "60067867890", 
             "Price per square meter": 54152}
             ]):
        last_week(today_date)
        ans = {"Address": {0: 'Особняк на Александрова, 18'},
             "Link": {0: "https://osobnyaki.com//na-nikoloyamskoy-49s2"}, 
             "Date added": {0: "2021-12-16"}, 
             "Square": {0: 1788}, 
             "Price": {0: 60067867890}, 
             "Price per square meter": {0: 54152}} 
        df = pd.read_excel('info_excel_week.xlsx').to_dict()
        assert df == ans

def test_last_kvartal():
    """Тест проверяет, что в эксель записываются данные только за прошедшие 3 месяца"""
    with unittest.mock.patch(
        'main.get_data',
         return_value=[
             {"Address": 'Особняк на Николоямской, 49с2',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2021-12-17", 
             "Square": "1108", 
             "Price": "60000000", 
             "Price per square meter": 54152},
             {"Address": 'Особняк на Александрова, 18',
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": "2021-09-13", 
             "Square": "1788", 
             "Price": "60067867890", 
             "Price per square meter": 54152}
             ]):
        last_kvartal(today_date)
        ans = {"Address": {0: 'Особняк на Александрова, 18'},
             "Link": {0: "https://osobnyaki.com//na-nikoloyamskoy-49s2"}, 
             "Date added": {0: "2021-09-13"}, 
             "Square": {0: 1788}, 
             "Price": {0: 60067867890}, 
             "Price per square meter": {0: 54152}} 
        df = pd.read_excel('info_excel_three_month.xlsx').to_dict()
        assert df == ans

def test_get_page_soup():
    """Тест проверяет, что сайт принимает запрос"""
    main_url = 'https://osobnyaki.com/'
    assert get_page_soup(main_url)[1] == '<Response [200]>'

def test_get_key():
    """Тест проверяет, что найден корректный токен сессии"""
    main_url = 'https://osobnyaki.com/'
    key = get_key(main_url)
    assert len(key) == 40

def test_get_osobnyak_links():
    """Тест проверяет, при основном парсинге извлекаются все данные и POST - запрос отправлен успешно"""
    main_url = 'https://osobnyaki.com/'
    key = get_key(main_url)
    osobnyak_links, dates, prices, gabarits, titles, answers = get_osobnyak_links(20, 0, key)
    flag = True
    for i in answers:
        if i != '<Response [200]>':
            flag = False
    assert flag == True
    assert len(osobnyak_links) == 20
    assert len(dates) == 20
    assert len(prices) == 20
    assert len(gabarits) == 20
    assert len(titles) == 20

def test_info():
    """Тест проверяет, что словарь с данными о каждом особняке формируется корректно"""
    assert info('https://osobnyaki.com//na-trifonovskoy-ulitse-28', '2020-08-30', '60000000', '1108', 'Александрова, 18') == {'Address': 'Александрова, 18', 'Link': 'https://osobnyaki.com//na-trifonovskoy-ulitse-28', 
    'Date added': '2020-08-30', 'Square': '1108', 'Price': '60000000', 'Price per square meter': 54152}
    assert info('https://osobnyaki.com//na-trifonovskoy-ulitse-28', '2020-08-30', None, None, 'Александрова, 18') == {'Address': 'Александрова, 18', 'Link': 'https://osobnyaki.com//na-trifonovskoy-ulitse-28', 
    'Date added': '2020-08-30', 'Square': None, 'Price': None, 'Price per square meter': None}

def test_main_s():
    """Тест проверяет, что список словарей, в которых хранится информация об особняках, формируется корректно"""
    with unittest.mock.patch(
        'main.get_osobnyak_links',
         return_value=[
             ['https://osobnyaki.com//na-trifonovskoy-ulitse-28', "https://osobnyaki.com//na-nikoloyamskoy-49s2"], 
             ["2021-09-13", '2020-08-30'], 
             ['60000000', "87000000"], 
             ['1108', "1678"], 
             ['Особняк на Александрова, 18', "Особняк на Мира, 106"],
             ['<Response [200]>', '<Response [200]>']
             ]):
        list_info = main_s()
        ans = [
            {"Address": 'Особняк на Александрова, 18',
             "Link": 'https://osobnyaki.com//na-trifonovskoy-ulitse-28', 
             "Date added": "2021-09-13", 
             "Square": '1108', 
             "Price": '60000000', 
             "Price per square meter": 54152},
             {"Address":  "Особняк на Мира, 106",
             "Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", 
             "Date added": '2020-08-30', 
             "Square": "1678", 
             "Price": "87000000", 
             "Price per square meter": 51847}
             ] 
        assert ans == list_info





