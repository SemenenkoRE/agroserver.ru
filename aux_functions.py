import time
import datetime

def print_error(reference_ad, exception):

    """ Выводит на экран ошибку """

    print(f'ссылка: {reference_ad}\n')
    print(f'ошибка: {exception}')

def save_errors(reference_ad, exception):

    """
    Функция переодически может встречаться с ошибки, необходимые для дальнейшего анализа.
    Для их сохранения применяется функция записи текста ошибки в отдельный текстовый файл.
    """

    with open('errors', 'a', encoding='utf-8') as er:
        er.write(f'ссылка: {reference_ad}\n')
        er.write(f'ошибка: {exception}\n\n')


def set_price(price_ad):

    """ Функция принимает текст с информацией о цене, отдает ответ в виде валюты, стоимости или ст-ти до / после  """

    unit_price = None

    if 'usd' in price_ad:
        unit_price = 'долл.'
    elif 'euro' in price_ad:
        unit_price = 'евро'
    else:
        unit_price = 'рубль'

    price_lower = None
    price_upper = None
    price_alone = None

    # 1. Цена в виде диапазона

    try:

        if price_ad == '':
            pass
        elif 'договорн' in price_ad:
            pass
        elif '—' in price_ad:
            list_piece = price_ad.split('—')
            price_lower = treat_price_ad(list_piece[0])
            price_upper = treat_price_ad(list_piece[1])
            price_alone = 0

        elif 'от' in price_ad:
            price_lower = treat_price_ad(price_ad)
            price_upper = 0
            price_alone = 0

        elif 'шт' in price_ad:
            price_lower = 0
            price_upper = 0
            price_alone = treat_price_ad(price_ad)

    except Exception as error:
        print(f'error in set_price: {error}')

    return unit_price, price_alone, price_lower, price_upper

def treat_price_ad(text):

    price = ''

    for i in text:

        if i.isdigit():
            price = price + i

    return float(price)


# ************************************************************************************************************

def binary_response(text):

    """
    Функция получает текст в обычном виде и возвращает текст в формате двоичного кода.
    Опред-ся соотвестствующий элементу текста номер в юникоде, который далее приводится к бинарному (двоичному) виду.
    """

    bin_text = ''

    for letter in text:
        bin_text = f"{bin_text}{ord(letter):b} "  # цифра переводится в двоичный код с помощью f-строки и опции :b

    return bin_text


def clearing_unnecessary_symbols(bin_text):
    """ Бинарный текст очищается от элементов, соответствующих \n и \t. """

    bin_text_list = bin_text.split(' ')

    for el in reversed(range(len(bin_text.split(' ')))):

        if bin_text_list[el] == '1010' or bin_text_list[el] == '1001':
            bin_text_list.pop(el)

    bin_text_correct = ''

    for number, el in enumerate(bin_text_list):

        if '1' in el or '0' in el:

            if number != len(bin_text_list) - 1:
                bin_text_correct = f'{bin_text_correct}{el} '

    return bin_text_correct


def text_response(bin_text):
    """ Функция принимает текст в бинарном виде и возращает в нормальном.  """

    text = ''

    for element in bin_text.split(' '):

        if '0' in element or '1' in element:
            text = f"{text}{chr(int(element, 2))}"

    return text


def processing_text(text):
    """
    Функция получает текст, через приведение к двоичному коду удаляет символы \n и \t, возвращает к текстовому формату.
    """

    bin_text = binary_response(text)
    bin_text_correct = clearing_unnecessary_symbols(bin_text)
    text = text_response(bin_text_correct)

    return text

# ************************************************************************************************************

months_dict_en = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
                      'Oct': 10, 'Nov': 11, 'Dec': 12}

months_dict_rus = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
                   'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12}


def set_time_ad(text_time):
    """
        Определение даты и времени объявления.
        Особенности: метод приводит дату к виду формата sql -- datetime
    """

    day, month, year, hh, mm, ss = None, None, None, None, None, None

    if 'сегодня' in text_time.lower():
        if len(time.ctime().split(' ')) == 5:
            day = int(time.ctime().split(' ')[2])
            year = int(time.ctime().split(' ')[4])
        elif len(time.ctime().split(' ')) == 6:
            day = int(time.ctime().split(' ')[3])
            year = int(time.ctime().split(' ')[5])

        for key, val in months_dict_en.items():

            if time.ctime().split(' ')[1] == key:
                month = val

        # set time
        hh, mm, ss = set_time(text_time)


    elif 'вчера' in text_time.lower():

        if time.ctime(time.time() - 24 * 3600).split(' ')[2] != "":
            day = int(time.ctime(time.time() - 24 * 3600).split(' ')[2])
            year = int(time.ctime(time.time() - 24 * 3600).split(' ')[4])
        elif time.ctime(time.time() - 24 * 3600).split(' ')[2] == "":
            day = int(time.ctime(time.time() - 24 * 3600).split(' ')[3])
            year = int(time.ctime(time.time() - 24 * 3600).split(' ')[5])

        for key, val in months_dict_en.items():

            if time.ctime(time.time() - 24 * 3600).split(' ')[1] == key:
                month = val
                break

        # set time
        hh, mm, ss = set_time(text_time)

    else:

        # set correct day
        day = int(text_time.split()[0])

        # set correct month
        month = None
        for key, val in months_dict_rus.items():

            if key == text_time.split()[1].lower():
                month = val
                break

        # set correct year
        year = 2022

        # set time
        hh, mm, ss = 0, 0, 0

    return datetime.datetime(year, month, day, hh, mm, ss)


def set_time(untreated_time_offer):

    # set hours
    hh = int(untreated_time_offer.split()[-1].split(":")[0])

    # set minutes
    mm = int(untreated_time_offer.split()[-1].split(":")[1])

    # set seconds
    ss = 0

    return hh, mm, ss


if __name__ == '__main__':
    print(set_price('цена: 7 800 000 — 8 300 000 руб / шт'))
    # print(set_time_ad('04 Февраля 2022'))
    pass


