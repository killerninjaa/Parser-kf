from tkinter import *
from seleniumwire import webdriver
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup, Comment
from datetime import date
import json
from PIL import ImageTk, Image

flag = False
today_date = str(date.today())

def get_data():
    """Получить данные о особняках. Если данные уже собраны,
    то выгрузить их. Если нет, то запустить парсинг и записать данные в файл для хранения
    :return list_info: список словарей, где каждый словарь содержит инфу о конкретном особняке
    """
    global flag
    if flag == False:
        list_info = main_s()
        file = open("list_info.txt", 'w')
        json.dump(list_info, file, indent = 6)
        flag = True
    else:
        file = open("list_info.txt", 'r')
        list_info = json.load(file)
    return list_info

def find_ch(ch, num):
    """Сформировать число в требуемом формате
    :param ch: число, сегодняшнее число
    :param num: число, сдвиг по дате
    :return: строка, число в необходимом формате
    """
    if len(str(ch - num)) == 1:
        return '0' + str(ch - num)
    else: 
        return str(ch - num)
    
def find_mes(mes, num):
    """Сформировать месяц в требуемом формате
    :param mes: число, сегодняшний месяц
    :param num: число, сдвиг по месяцу
    :return: строка, месяц в необходимом формате 
    """
    if len(str(mes - num)) == 1:
        return '0' + str(mes - num)
    else: 
        return str(mes - num)

def all_time():
    """Записать данные об особняках в таблицу эксель"""
    global flag
    list_info = get_data()
    osobnyak_info_df = pd.DataFrame(list_info)
    writer = pd.ExcelWriter('info_excel_all.xlsx', engine='xlsxwriter')
    osobnyak_info_df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()    

def this_year(today_date):
    """Отобрать особняки, добавленные в нынешнем году, и записать в эксель"""
    global flag  
    list_info = get_data() 
    list_info_new = []
    for oso_dict in list_info:
        if oso_dict['Date added'][:4] == today_date[:4]:
            list_info_new.append(oso_dict)
    osobnyak_info_df = pd.DataFrame(list_info_new)
    writer = pd.ExcelWriter('info_excel_year.xlsx', engine='xlsxwriter')
    osobnyak_info_df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    return list_info_new

def last_month(today_date):
    """Отобрать особняки, добавленные в прошлом месяце, и записать в эксель"""
    global flag
    list_info = get_data() 
    list_info_new = []
    for oso_dict in list_info:
        if today_date[5:7] == '01':
            if oso_dict['Date added'][5:7] == '12' and oso_dict['Date added'][:4] == str(int(today_date[:4]) - 1):
                list_info_new.append(oso_dict)
        elif oso_dict['Date added'][5:7] == str(int(today_date[5:7]) - 1) and oso_dict['Date added'][:4] == today_date[:4]:
            list_info_new.append(oso_dict)
    osobnyak_info_df = pd.DataFrame(list_info_new)
    writer = pd.ExcelWriter('info_excel_month.xlsx', engine='xlsxwriter')
    osobnyak_info_df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

def last_week(today_date):
    """Отобрать особняки, добавленные за последние 7 дней, и записать в эксель"""
    global flag
    list_info = get_data()   
    list_info_new = []
    for oso_dict in list_info:    
        if oso_dict['Date added'][5:7] == today_date[5:7] and oso_dict['Date added'][:4] == today_date[:4]:
            if int(today_date[8:10]) <= 7:
                if oso_dict['Date added'][8:10] == '01' or oso_dict['Date added'][8:10] == '02' or oso_dict['Date added'][8:10] == '03' or oso_dict['Date added'][8:10] == '04'or oso_dict['Date added'][8:10] == '05' or oso_dict['Date added'][8:10] == '06' or oso_dict['Date added'][8:10] == '07':
                    list_info_new.append(oso_dict)
            else:
                ch = int(today_date[8:10])
                if oso_dict['Date added'][8:10] == find_ch(ch, 1) or oso_dict['Date added'][8:10] == find_ch(ch, 2) or oso_dict['Date added'][8:10] == find_ch(ch, 3) or oso_dict['Date added'][8:10] == find_ch(ch, 4) or oso_dict['Date added'][8:10] == find_ch(ch, 5) or oso_dict['Date added'][8:10] == find_ch(ch, 6) or oso_dict['Date added'][8:10] == find_ch(ch, 7):
                    list_info_new.append(oso_dict)
    osobnyak_info_df = pd.DataFrame(list_info_new)
    writer = pd.ExcelWriter('info_excel_week.xlsx', engine='xlsxwriter')
    osobnyak_info_df.to_excel(writer, sheet_name='Sheet1')
    writer.save()        
    
def last_kvartal(today_date):
    """Отобрать особняки, добавленные за последние 3 месяца, и записать в эксель"""
    global flag
    list_info = get_data()    
    list_info_new = []
    for oso_dict in list_info: 
        if oso_dict['Date added'][:4] == today_date[:4]:
            if int(today_date[5:7]) <= 3:
                if oso_dict['Date added'][5:7] == '01' or oso_dict['Date added'][5:7] == '02' or oso_dict['Date added'][5:7] == '03':
                    list_info_new.append(oso_dict)
            else:
                mes = int(today_date[5:7])
                if  oso_dict['Date added'][5:7] == find_mes(mes, 1) or oso_dict['Date added'][5:7] == find_mes(mes, 2) or oso_dict['Date added'][5:7] == find_mes(mes, 3):
                    list_info_new.append(oso_dict)
    osobnyak_info_df = pd.DataFrame(list_info_new)
    writer = pd.ExcelWriter('info_excel_three_month.xlsx', engine='xlsxwriter')
    osobnyak_info_df.to_excel(writer, sheet_name='Sheet1')
    writer.save()     

def get_page_soup(url_link):
        """Функция, возвращающая html - дерево по адресу сайта
        :param url_link: строка, ссылка на сайт
        :return page_soup: объект BeautifulSoup, документ в виде вложенной структуры данных
        """
        response = requests.get(url_link)
        print(response)
        html = response.content
        page_soup = BeautifulSoup(html, 'html.parser')
        return page_soup, str(response)

def get_key(url_link):
    """Функция, возвращающая токен сессии сайта
    Необходим для выгрузки содержимого страницы
    с помощью отправки Post запроса серверу
    Для получения ключа с помощью бота жмем на кнопку, затем получаем содержимое
    журнала, в котором после нажатия на кнопку находит ключ
    :param url_link: строка, ссылка на сайт
    :return key: строка, ключ 
    """
    options = webdriver.ChromeOptions()
    options.headless = True    
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    driver.get(url_link)
    button = driver.find_element_by_class_name('cookie-button')
    button.click()
    time.sleep(5)
    button = driver.find_element_by_id('content_sws')
    button.click()
    time.sleep(9)
    for request in driver.requests:
        if 'https://osobnyaki.com/assets/components/msearch2/custom_action.php' == str(request.url):
            key = str(request.body)
            key = key[key.find('key=') + 4:-1]  
    return key

def get_osobnyak_links(num_of_oso, help, key):
    """Функция, осуществляющая парсинг
    Она обрабатвает все страницы сайта
    С каждой страницы она достает с сайта ссылку, адрес, дату добавления, цену, площадь каждого особняка
    :param num_of_oso: число, количество особняков на сайте
    :param help: число, вспомогательная переменная корректной работы цикла
    :param key: строка, токен сессии, передается в аргументах post - запроса
    :return osobnyak_links: список ссылок на все особняки
    :return dates: список дат добавления всех особняков
    :return prices: список цен всех особняков
    :return gabarits: список площадей каждого особняка
    :return titles: список адресов каждого особняка
    """
    dates = []
    osobnyak_links = []   
    prices = []
    gabarits = []
    titles = []
    answers = []

    for i in range(num_of_oso // 10 + help):
        
        payload = {'sort': 'tv|sdan:asc,tv|prodan:asc,ms|price:asc', 'page': str(i + 1), 'action': 'filter', 'pageId': '1', 'key': key}
        r = requests.post("https://osobnyaki.com/assets/components/msearch2/custom_action.php", data=payload)
        p = r
        r = r.json()
        page_soup = r['data']['results']
        page_soup = BeautifulSoup(page_soup, 'html.parser')
        
        for comments in page_soup.findAll(text=lambda text:isinstance(text, Comment)):
            stroki = str(comments.extract()).split('\n')
            for stroka in stroki:
                if ('2021' in stroka or '2020' in stroka or '2019' in stroka or '2018' in stroka or '2017' in stroka) and len(stroka) < 20:
                    dates.append(stroka[4:])          
        
        osobnyaki = page_soup.find_all('div', {'class': 'img t4'})
        for link in osobnyaki:
            osobnyak_links.append('https://osobnyaki.com/' + link.find('a').get('href'))    
        
        prices_small = page_soup.find_all('div', {'class': 'item_buy_price'})
        for price_small in prices_small:
            price_small = price_small.find_all('span', {'class': 'Houseprice'})
            for price in price_small:
                price = str(price.text)
                price = price[15:][::-1]
                price = price[13:][::-1]   
                price = price.replace(' ', '')
                prices.append(price)
        
        gabarits_all = page_soup.find_all('div', {'class': 'houseFullInfo'})
        for gabarits_small in gabarits_all:
            gabarits_small = gabarits_small.find('span')
            gabarits_small = gabarits_small.text
            gabarits_small = gabarits_small[:-3]
            gabarits.append(gabarits_small)
        
        titles_all = page_soup.find_all('div', {'class': 'title'})
        for title in titles_all:
            title = title.text
            title = title[18:]
            title = title[:-27]
            titles.append(title)

        answers.append(str(p))
    
    return osobnyak_links, dates, prices, gabarits, titles, answers

def info(osobnyak_link, date, price, gabarit, title):
    """Функция, фоормирующая для каждого особняка словарь с информацией о нем
    Словарь содержит адрес, ссылку, дату добавления, площадь, цену и цену за квадратный метр
    :param osobnyak_link: строка, ссылка на особняк
    :param date: строка, дата добавления
    :param price: строка, цена особняка
    :param gabarit: строка, площадь особняка
    :param title: строка, адрес особняка
    :return osobnyak_info: словарь с информацией об особняке
    """
    try:
        price_for_one_gabarit = round(int(price) / int(gabarit))
    except:
        price_for_one_gabarit = None

    osobnyak_info = {
        'Address': title,
        'Link': osobnyak_link, 
        'Date added': date,
        'Square': gabarit,
        'Price': price,
        'Price per square meter': price_for_one_gabarit
    }

    return osobnyak_info

def main_s():
    """Главная функция, в которой происходит парсинг
    :return list_info: список словарей, где каждый словарь содержит инфу о конкретном особняке
    """
    main_url = 'https://osobnyaki.com/'

    page_soup_main = get_page_soup(main_url)[0]

    num_of_oso = int(page_soup_main.find('span', {'id': 'mse2_total'}).text)
    if num_of_oso % 10 == 0:
        help = 0
    else:
        help = 1

    key = get_key(main_url)
    osobnyak_links, dates, prices, gabarits, titles, answers = get_osobnyak_links(num_of_oso, help, key)

    num = 0
    list_info = []
    for link in osobnyak_links:
        list_info.append(info(link, dates[num], prices[num], gabarits[num], titles[num]))
        num += 1
    
    return list_info

if __name__ == "__main__":
    
    def on_enter(e):
        e.widget['fg'] = '#808080'

    def on_leave(e):
        e.widget['fg'] = '#000000'

    root = Tk()
    root.title('Knight Frank Parser')
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    w = w // 2 # середина экрана
    h = h // 2
    w = w - 320 # смещение от середины
    h = h - 215
    root.geometry('640x430+{}+{}'.format(w, h))
    root["bg"] = "#FFFFFF"
    img = ImageTk.PhotoImage(Image.open("kf-logo.png"))
    logo = Label(image = img, bg='#FFFFFF')
    parser_label = Label(text='PARSER', bg='#FFFFFF', fg='#D0103A')
    parser_label.config(font=("Helvetica", 30))
    kf_label = Label(text='KNIGHT FRANK', bg='#FFFFFF', fg='#D0103A')
    kf_label.config(font=("Helvetica", 30))
    period_label = Label(text='ВЫБРАТЬ ПЕРИОД:', bg='#FFFFFF', fg='#808080')
    period_label.config(font=("Helvetica", 16))

    butAllTime = Button(text="Все время", bg='#FFFFFF', highlightthickness = 0, bd = 0)
    butAllTime.config(font=("Helvetica", 19))
    butThisYear = Button(text="Год", bg='#FFFFFF', highlightthickness = 0, bd = 0)
    butThisYear.config(font=("Helvetica", 19))
    butLastMonth = Button(text="Месяц", bg='#FFFFFF', highlightthickness = 0, bd = 0)
    butLastMonth.config(font=("Helvetica", 19))
    butLastWeek = Button(text="Неделя", bg='#FFFFFF', highlightthickness = 0, bd = 0)
    butLastWeek.config(font=("Helvetica", 19))
    butLastKv = Button(text="Квартал", bg='#FFFFFF', highlightthickness = 0, bd = 0)
    butLastKv.config(font=("Helvetica", 19))

    butAllTime.bind("<Enter>", on_enter)
    butAllTime.bind("<Leave>", on_leave)
    butThisYear.bind("<Enter>", on_enter)
    butThisYear.bind("<Leave>", on_leave)
    butLastKv.bind("<Enter>", on_enter)
    butLastKv.bind("<Leave>", on_leave)
    butLastWeek.bind("<Enter>", on_enter)
    butLastWeek.bind("<Leave>", on_leave)
    butLastMonth.bind("<Enter>", on_enter)
    butLastMonth.bind("<Leave>", on_leave)
    butLastKv.bind("<Enter>", on_enter)
    butLastKv.bind("<Leave>", on_leave)

    butAllTime.bind('<Button-1>', lambda e: all_time())
    butThisYear.bind('<Button-1>', lambda e: this_year(today_date))
    butLastMonth.bind('<Button-1>', lambda e: last_month(today_date))
    butLastWeek.bind('<Button-1>', lambda e: last_week(today_date))
    butLastKv.bind('<Button-1>', lambda e: last_kvartal(today_date))

    logo.pack(anchor=W, padx=17, pady=10)
    parser_label.pack(anchor=W, padx=14, pady=0)
    kf_label.pack(anchor=W, padx=14, pady=0)
    period_label.pack(anchor=W, padx=16, pady=(16, 0))
    butAllTime.pack(anchor=W, padx=11)
    butThisYear.pack(anchor=W, padx=11)
    butLastKv.pack(anchor=W, padx=11)
    butLastMonth.pack(anchor=W, padx=11)
    butLastWeek.pack(anchor=W, padx=11)
    root.mainloop()

