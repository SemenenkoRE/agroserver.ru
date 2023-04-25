from proxy_connection import Proxy
from research_header import ResearchHeader
import aux_functions as af
import hashlib
from pymongo import MongoClient
from db_use import SqlAddAgroserverTechnic, SqlDataBaseQuery
import random
import time
import list_parsing as lp
import datetime

class AgroserverResearch():

    """ Парсинг предложений на сайте agroserver.ru """

    # Название бызы MongoDB
    name_data_base = 'data_base_agroserver'

    # Переменная содержит объект базы данных MongoDB
    data_base = None

    #
    check_id = None

    # Вид запрашиваемой техники
    mode = None

    # Страница с результатами поиска
    research_reference = None

    # DOM поисковой страницы
    dom_research = None

    # DOM страницы со списком объявлений компании
    dom_list = None

    # DOM страницы с объявлением
    dom_ad = None

    #
    list_companies = None

    # Ссылка для тракторов (без номера страницы)
    ref_traktor = 'https://agroserver.ru/traktory/Y2l0eT18cmVnaW9uPXxjb3VudHJ5PXxtZXRrYT0yODQsMjg1LDI4NiwyODcsMjg5LDYsMjkwLDM1LDQ4OCwzMDB8c29ydD0x/'
    ref_combainer = 'https://agroserver.ru/kombayny/Y2l0eT18cmVnaW9uPXxjb3VudHJ5PXxtZXRrYT18c29ydD0x/'

    #
    response_text = ''
    expr_l_s = ['л.с.', 'л. с.', ' л с ', ' л с,', ' лс ', ' лс,', 'л.с', 'л/с']

    unique_id = None
    reference_ad = None
    type_technic = None
    traktor_base = None
    maker_technic = None
    model_technic = None
    year_make = None
    power_engine = None
    condition_technic = None
    address = None
    company = None
    moto_hours = None

    price_alone = None
    price_lower = None
    price_upper = None
    price_unit = None

    header_ad = None
    offer_datetime = None
    reference_list = None

    def __init__(self, mode):

        self.mode = mode

    def get_data(self):

        # Установить соединение с базой данных
        self.set_db_mongo()

        self.time_wait()

        # Получить сведения
        self.research_main()


    def set_dom_research(self, current_page):

        """ Метод устанавливает:
        1. ссылку на поисковую (начальную) страницу
        2. Метод устанавливает dom поисковой страницы
        """

        # Формирование поисковой страницы
        if self.mode == 'traktor':
            self.research_reference = self.ref_traktor + str(current_page) + '/'
            self.list_companies = lp.list_companies_traktor
        elif self.mode == 'combainer':
            self.research_reference = self.ref_combainer + str(current_page) + '/'
            self.list_companies = lp.list_companies_combainer

        # Создание dom страницы
        self.dom_research = self.get_dom(self.research_reference)

    def research_main(self):

        """  """

        # 1. Открыть все отдельные списки компаний с предложениями

        for ref in self.list_companies:
            # Получить ссылку на страницу со списком объявлений
            self.reference_list = ref

            # Получить dom на страницу со списком объявлений
            self.dom_list = self.get_dom(self.reference_list)

            # Исследование всех объявлений из списка объявлений компании
            self.research_list_company()

        # 2. Получение ссылок на все объекты со страницы с выгрузкой

        # Установить dom запроса поисковой страницы
        self.set_dom_research(1)

        # После парсинга первой страницы определяем количество поисковых страниц всего
        count = len(self.dom_research.xpath("//ul[@class='pg']/li/"))

        for i in range(2, count + 1):

            # Установить dom запроса поисковой страницы
            self.set_dom_research(i)

            for ref in self.dom_research.xpath("//div[@class='list_full']//div[@class='line']//div[@class='th']/a/@href"):

                self.reference_ad = f"https://agroserver.ru{ref}"

                # Получить dom на страницу с объявлением
                self.dom_ad = self.get_dom_ad(self.reference_ad)

                self.research_ad()

                self.time_wait()

    def set_data_intro_research_page(self):

        for ref in self.dom_research.xpath("//div[@class='list_full']//div[@class='line']//div[@class='th']/a/@href"):

            self.reference_ad = f"https://agroserver.ru{ref}"

            # Получить dom на страницу с объявлением
            self.dom_ad = self.get_dom_ad(self.reference_ad)

            self.research_ad()

            self.time_wait()

            # Получение ссылок из дополнительных списков внутри объявления

        for ref in self.dom_research.xpath("//div[@class='list_full']//div[@class='line']//ul[@class='list']//a/@href"):

            # Получить ссылку на страницу со списком объявлений
            self.reference_ad = f'https://agroserver.ru{ref}'

            # Получить dom на страницу с объявлением
            self.dom_ad = self.get_dom_ad(self.reference_ad)

            # Проверяем есть ли цена в тексте объявления
            self.research_ad()

            self.time_wait()

    def research_list_company(self):

        """ Исследование объявлений со страницы со списком объявлений """

        self.time_wait()

        for ref in self.dom_list.xpath("//ul[@class='b_list_user']//li[@class='th']/a/@href")[-1:]:

            # Получить ссылку на объявление
            self.reference_ad = f"https://agroserver.ru{ref}"

            # Получить dom на страницу с объявлением
            self.dom_ad = self.get_dom_ad(self.reference_ad)

            self.research_ad()

            self.time_wait()

    def research_ad(self):

        """ Исследование данных со страницы объявления

        Необходимо будет написать декоратор !!!

        """

        # Получение текста заголовка
        self.header_ad = self.dom_ad.xpath("//h1/text()")[0]

        # Получение даты объявления
        temp = self.dom_ad.xpath("//div[@class='date']/div/text()")[0]
        self.offer_datetime = af.set_time_ad(temp)

        # Получение сведений из заголовка
        data_header = ResearchHeader(self.header_ad, 'traktor')

        self.type_technic, self.traktor_base, self.maker_technic, self.model_technic, self.year_make, \
            self.power_engine, self.condition_technic = data_header.return_result()

        # Определение размера стоимости
        try:
            untreated_price = self.dom_ad.xpath("//div[@class='mprice']/text()")[0]
            self.price_unit, self.price_alone, self.price_lower, self.price_upper = af.set_price(untreated_price)
        except Exception as error:
            self.price_unit = 'рубль'
            print(f'ОШИБКА: {error}\nЛИСТ: {self.reference_list}\nОБЪЯВЛЕНИЕ: {self.reference_ad}')

        # Определение адреса
        temp = self.dom_ad.xpath("//div[@class='bl ico_location']/text()")[0]
        self.address = af.processing_text(temp)

        # Определение компании
        self.company = self.dom_ad.xpath("//a[@class='personal_org_menu ajs']/text()")[0]

        # Получить текст для дальнейшего анализа
        text_ad = self.dom_ad.xpath("//div[@class='text']/text()")[0]

        # 1. Проверка наличия года выпуска в тексте

        if self.year_make is None:
            for j in range(1982, 2023):
                if str(j) in text_ad:
                    self.year_make = j

                    if self.condition_technic is None and self.year_make < 2021:
                        self.condition_technic = 'б/у'

                    break

        # 2. Проверка наличия информации о лошадиных силах

        if self.power_engine is None:
            for j in self.expr_l_s:
                if j in text_ad:

                    index = text_ad.index(j)

                    if index > 4:

                        temp = ''

                        for q in text_ad[index-4 : index]:

                            if q.isdigit():
                                temp = temp + q

                        if temp != '':
                            self.power_engine = float(temp)

                    break

        # 3. Проверка на наличие указания о состоянии и моточасах

        if 'гарант' not in text_ad:

            expr_mh = ['наработка', 'м.ч', 'м/ч', 'м. ч']

            for q in expr_mh:
                if q in text_ad:

                    temp = ''
                    index = text_ad.index(q)

                    if q != 'наработка':
                        for q in text_ad[index-7 : index]:

                            if q.isdigit():
                                temp = temp + q

                    else:
                        for q in text_ad[index : index + 8]:

                            if q.isdigit():
                                temp = temp + q

                    if temp != '':
                        self.moto_hours = float(temp)

                        if self.condition_technic is None:
                            self.condition_technic = 'б/у'

        # Создать hex_code
        self.get_cript_id()

        # Передача полученных результатов в БД
        self.add_to_bd()

        # Показать результат
        self.print_result()

        # Обнулить сведения
        self.clean_result()

        # Сделать паузу перед парингом следующего объекта
        self.time_wait()

    def clean_result(self):

        # Обнуление сведений

        self.reference_ad = None
        self.type_technic = None
        self.traktor_base = None
        self.maker_technic = None
        self.model_technic = None
        self.year_make = None
        self.power_engine = None
        self.condition_technic = None
        self.address = None
        self.price_alone = None
        self.price_lower = None
        self.price_upper = None
        self.price_unit = None
        self.moto_hours = None
        self.header_ad = None
        self.offer_datetime = None

    def print_result(self):

        """ Показать результат """

        print(f'reference_ad_: {self.reference_ad}')
        print(f'type_technic_: {self.type_technic}')
        print(f'traktor_base_: {self.traktor_base}')
        print(f'maker_technic: {self.maker_technic}')
        print(f'model_technic: {self.model_technic}')
        print(f'year_make____: {self.year_make}')
        print(f'power_engine_: {self.power_engine}')
        print(f'condition_technic: {self.condition_technic}')
        print(f'address______: {self.address}')
        print(f'price_alone__: {self.price_alone}')
        print(f'price_lower__: {self.price_lower}')
        print(f'price_upper__: {self.price_upper}')
        print(f'price_unit___: {self.price_unit}')
        print(f'moto_hours___: {self.moto_hours}')
        print(f'header_ad____: {self.header_ad}')
        print(f'offer_datetime: {self.offer_datetime}')

    @staticmethod
    def get_dom(reference_list):

        """ Получить dom """

        connect = Proxy(reference_list)
        # dom = connect.get_dom_own_ip()
        dom = connect.get_dom()
        return dom

    @staticmethod
    def get_dom_ad(reference_list):

        """ Получить dom """

        connect = Proxy(reference_list)
        # dom = connect.get_dom_own_ip()
        dom = connect.get_dom()
        return dom

    def set_db_mongo(self):

        """ Создание подключения к MongoDB """

        client = MongoClient('localhost', 27017)
        db = client[self.name_data_base]
        self.data_base = db.data_base

    def get_cript_id(self):

        """ Создание уникального специально хеш кода для проверки на наличие данного объекта в БД """

        self.unique_id = hashlib.sha1(f'{self.reference_ad}{self.offer_datetime}{self.header_ad}'.encode('utf-8')).hexdigest()

    def add_to_bd(self):

        """ Если данный объект в базе не присутствует, то добавление происходит """

        for n in self.data_base.find({'hex_id': self.unique_id}):
            self.check_id = 'stop'

        if self.check_id != 'stop':

            # Получить номер последнего IP
            sql_query = SqlDataBaseQuery()
            last_id = sql_query.query_last_id()

            if last_id is None:
                last_id = 1

            # Добавить коллекции значений в БД
            self.add_object_sql(last_id)
            self.add_object_mongodb(last_id)

        else:
            print('ОБЪЕКТ В БД ИМЕЕТСЯ')

    def add_object_sql(self, last_id):

        """ Добавить коллекцию значений в БД SQL """

        sql_add = SqlAddAgroserverTechnic(id=last_id,
                                            hex_id=self.unique_id,
                                            reference_ad=self.reference_ad,
                                            header_ad=self.header_ad,
                                            type_technic=self.type_technic,
                                            price_alone=self.price_alone,
                                            price_lower=self.price_lower,
                                            price_upper=self.price_upper,
                                            price_unit=self.price_unit,
                                            offer_datetime=self.offer_datetime,
                                            address=self.address,
                                            model_technic=self.model_technic,
                                            year=self.year_make,
                                            condition=self.condition_technic,
                                            maker=self.maker_technic,
                                            moto_hours=self.moto_hours,
                                            power_engine=self.power_engine,
                                            traktor_base=self.traktor_base)

    def add_object_mongodb(self, last_id):

        """ Добавить коллекцию значений в БД MongoD """

        self.data_base.insert_one(
            {'_id': last_id, 'hex_id': self.unique_id, 'reference_ad': self.reference_ad,
             'header_ad': self.header_ad, 'type_technic': self.type_technic, 'price_alone': self.price_alone,
             'price_lower': self.price_lower, 'price_upper': self.price_upper, 'price_unit': self.price_unit,
             'offer_datetime': self.offer_datetime, 'address': self.address, 'model_technic': self.model_technic,
             'year': self.year_make, 'condition': self.condition_technic, 'maker': self.maker_technic,
             'moto_hours': self.moto_hours, 'power_engine': self.power_engine, 'traktor_base': self.traktor_base})

    @staticmethod
    def time_wait():

        """ Пауза между парсингом объявлений """
        time_wait = random.randint(70, 120)
        time.sleep(time_wait)


if __name__ == '__main__':

    result = AgroserverResearch('traktor')
    result.get_data()


