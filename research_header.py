import list_technic as lt

expr_l_s = ['л.с.', 'л. с.', ' л с ', ' л с,', ' лс ', ' лс,', 'л.с', 'л/с']

special_symbols = ['.', '_', '/', '-']

class ResearchHeader():

    """ Класс анализирует заголовок объявления и возращает готовые параметры """

    SYMBOLS_CHANGE_SPACE = [' (', ') ', '" ', ' "', ', ', ' ,']
    SYMBOLS_CHANGE = ['(', ')', ',', '"', ';']

    MODE_RESEARCH = None

    TYPES_TECHNIC = lt.list_type
    MAKER_TECHNIC = lt.list_maker_traktor

    type_technic = None
    traktor_base = None
    maker_technic = None
    model_technic = None
    year_make = None
    power_engine = None
    condition_technic = None

    text_header = None

    def __init__(self, text_header, mode_research):

        self.MODE_RESEARCH = mode_research

        self.text_header = text_header

        # Очистка текста заголовка
        self.clean_text()

        # Основная обработка
        self.set_parameters()

        # # Печать результата
        # self.print_result()

    def set_parameters(self):

        """ Устанавливаем режим того, какую технику изучаем """

        if self.MODE_RESEARCH == 'traktor':

            self.research_parameters()

    def clean_text(self):

        """ Метод очищает текст заголовка от лишних и вредящих символов """

        # 1. Очистка текста от лишних элементов в связке с пробелом

        for el in self.SYMBOLS_CHANGE_SPACE:

            while True:

                if el in self.text_header:
                    self.text_header = self.text_header.replace(el, ' ')[:]
                else:
                    break

        # 2. Замена оставшихся символов на ''

        for el in self.SYMBOLS_CHANGE:

            while True:

                if el in self.text_header:
                    self.text_header = self.text_header.replace(el, '')[:]
                else:
                    break

    def research_parameters(self):

        """  """

        research_list = []

        # Делим текст заголовка по пробелам

        if ' ' in self.text_header:
            research_list = self.text_header.split(' ')[:]
        else:
            research_list = [self.text_header][:]

        # Перебор элементов полученного списка

        for el in research_list:

            # Переменная status при значении False не проверяется далее
            status = True

            # 1. Проверка несет ли слово заголовка информацию о типе технике

            for j in self.TYPES_TECHNIC:

                if self.type_technic is None:

                    for q, w in j.items():

                        if self.type_technic is None:

                            for x in w:

                                if el.lower() == x:
                                    self.type_technic = q
                                    break

                        else:
                            status = False
                            break

            # 2. Проверка слова на наличие информации о том, на какой базе трактор

            if status is True:

                if 'колесн' in el or 'колёсн' in el:
                    self.traktor_base = 'колесный'
                    status = False

                elif 'гусеничн' in el:
                    self.traktor_base = 'гусеничный'
                    status = False

            # 3. Определение производителя

            if status is True:

                for j in self.MAKER_TECHNIC:

                    if status is True:

                        for q, w in j.items():

                            if status is True:

                                for x in w:

                                    # Проверка для названий производителя из 2х слов
                                    if ' ' in x:
                                        if x in self.text_header.lower():
                                            self.maker_technic = q
                                            status = False
                                            break
                                    else:

                                        if el.lower() == x:
                                            self.maker_technic = q
                                            status = False
                                            break

                                        elif x in el.lower():
                                            self.maker_technic = q

            # 4. Проверка на то, что в элементе не содержится информация о состоянии

            if status is True:
                if 'б/у' in el or 'б.у' in el:
                    self.condition_technic = 'б/у'

            # 5. Определение модели

            if status is True:

                # 1. Случай: el не является / является числом + проверяем, что это не год и л.с.

                if el.isdigit():

                    # Проверка, что число не является годом / иначе передаем значение другому параметру

                    for j in range(1982, 2023):
                        if float(el) == j:
                            self.year_make = j
                            status = False
                            break

                    # Проверка, что число не является лошадиными силами / иначе передаем значение другому параметру
                    if status is True:
                        for j in expr_l_s:
                            if j in self.text_header.lower():

                                # Проверка что слов, являющихся цифрами не больше чем 1

                                count_digit = 0

                                for x in self.text_header.split(' '):
                                    if x.isdigit():
                                        count_digit += 1

                                if count_digit == 1:

                                    self.power_engine = float(el)
                                    status = False
                                    break

                                else:
                                    if float(el) < 500:
                                        self.power_engine = float(el)
                                        status = False
                                        break
                                    else:
                                        if self.model_technic is not None:
                                            self.model_technic = f'{self.model_technic} {el}'
                                            status = False
                                        else:
                                            self.model_technic = el
                                            status = False


                    # Если проверку прошло, то значение передается параметру модели
                    if status is True:
                        if self.model_technic is not None:
                            self.model_technic = f'{self.model_technic} {el}'
                            status = False
                        else:
                            self.model_technic = el
                            status = False

                # 1. Случай _ соответствие признакам

                if status is True:

                    test_upper_case = True
                    test_lower_case = True
                    test_digit = True
                    test_upper_many = True
                    test_special_symbols = True

                    for j in el:

                        if j.isdigit():
                            test_digit = False

                        elif j.isupper():

                            if test_upper_case is False:
                                test_upper_many = False
                            else:
                                test_upper_case = False

                        elif j.isupper() is False:
                            test_lower_case = False

                        else:
                            for x in special_symbols:
                                if j == x:
                                    test_special_symbols = False

                    if (test_special_symbols is False and test_digit is False) or \
                            (test_upper_many is False) or \
                            (test_upper_case is False and test_digit is False) or \
                            (test_special_symbols is False and test_lower_case is False) or \
                            (test_lower_case is False and test_digit is False):

                        if self.model_technic is not None:
                            self.model_technic = f'{self.model_technic} {el}'
                            status = False
                        else:
                            self.model_technic = el
                            status = False

    def return_result(self):

        return self.type_technic, self.traktor_base, self.maker_technic, self.model_technic, self.year_make, \
                self.power_engine, self.condition_technic

    def print_result(self):

        print(f'тип техники  : {self.type_technic}')
        print(f'база         : {self.traktor_base}')
        print(f'производитель: {self.maker_technic}')
        print(f'модель       : {self.model_technic}')
        print(f'год выпуска  : {self.year_make}')
        print(f'мощность     : {self.power_engine}')
        print(f'состояние    : {self.condition_technic}')

if __name__ == '__main__':

    header = 'Трактор Беларус МТЗ 952.3 - 17/12 (952.3-0000010-094)'

    parameters = ResearchHeader(header, 'traktor')



