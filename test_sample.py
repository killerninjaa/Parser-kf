import pytest
import json
from main import find_ch, find_mes, get_data, this_year, all_time, last_month, last_week, last_kvartal, main_s, get_page_soup, get_key, get_osobnyak_links, info
import unittest
from unittest import mock
from mock import patch
import pandas as pd
from datetime import date

today_date = str(date.today())

def test_find_ch_z():
    assert find_ch(7, 2) == '05' 

def test_find_ch_nz():
    assert find_ch(13, 2) == '11'

def test_find_mes_z():
    assert find_mes(4, 3) == '01'

def test_find_mes_nz():
    assert find_mes(12, 1) == '11'

def test_get_data():
    get_data()
    file = open("list_info.txt", 'r')
    list_info = json.load(file)
    assert len(list_info) == 581

with unittest.mock.patch('main.get_data', return_value=[{"Address": 'Особняк на Николоямской, 49с2',"Link": "https://osobnyaki.com//na-nikoloyamskoy-49s2", "Date added": "2020-10-26", "Square": "1108", "Price": "60000000", "Price per square meter": 54152}]):
    def test_all_time():
        all_time()
        df = pd.read_excel('info_excel_all.xlsx')
        assert df.shape[0] == 1
    
def test_this_year():
    this_year(today_date)
    df = pd.read_excel('info_excel_year.xlsx')
    assert df.shape[0] == 71

def test_last_month():
    last_month(today_date)
    df = pd.read_excel('info_excel_month.xlsx')
    assert df.shape[0] == 5

def test_last_week():
    last_week(today_date)
    df = pd.read_excel('info_excel_week.xlsx')
    assert df.shape[0] == 2

def test_last_kvartal():
    last_kvartal(today_date)
    df = pd.read_excel('info_excel_three_month.xlsx')
    assert df.shape[0] == 20

def test_get_page_soup():
    main_url = 'https://osobnyaki.com/'
    assert get_page_soup(main_url)[1] == '<Response [200]>'

def test_get_key():
    main_url = 'https://osobnyaki.com/'
    key = get_key(main_url)
    assert len(key) == 40

def test_get_osobnyak_links():
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
    assert info('https://osobnyaki.com//na-trifonovskoy-ulitse-28', '2020-08-30', '60000000', '1108', 'Александрова, 18') == {'Address': 'Александрова, 18', 'Link': 'https://osobnyaki.com//na-trifonovskoy-ulitse-28', 
    'Date added': '2020-08-30', 'Square': '1108', 'Price': '60000000', 'Price per square meter': 54152}
    assert info('https://osobnyaki.com//na-trifonovskoy-ulitse-28', '2020-08-30', None, None, 'Александрова, 18') == {'Address': 'Александрова, 18', 'Link': 'https://osobnyaki.com//na-trifonovskoy-ulitse-28', 
    'Date added': '2020-08-30', 'Square': None, 'Price': None, 'Price per square meter': None}

def test_main_s():
    list_info = main_s()
    assert len(list_info) == 581





