import requests as r
from lxml import html
from requests.auth import HTTPProxyAuth
import random
import json


class Proxy():

    """  """

    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36', 'Accept': '*/*'}
    fake_user_agent = None


    def __init__(self, url):
        self.url = url

    # def get_dom_proxy(self):
    #
    #     """ Получить dom через прокси """
    #
    #     # self.header['User-Agent'] = self.fake_user_agent
    #
    #     session = r.Session()
    #     session.proxies = {'http': 'http://77.51.188.76:64053'}
    #     session.auth = HTTPProxyAuth('NyhVuE', 'PaXVEqYK5zYZ')
    #     response = session.get(self.url, headers=self.header)
    #     print(f'STATUS: {response.status_code}')
    #     dom = html.fromstring(response.text)
    #     return dom
    #
    # def get_dom_proxy_extr(self):
    #
    #     """ Получить dom через прокси """
    #
    #     # self.header['User-Agent'] = self.fake_user_agent
    #
    #     session = r.Session()
    #     session.proxies = {'http': 'http://77.51.188.76:64053'}
    #     session.auth = HTTPProxyAuth('NyhVuE', 'PaXVEqYK5zYZ')
    #     response = session.get(self.url, headers=self.header)
    #     print(f'STATUS: {response.status_code}')
    #     dom = html.fromstring(response.text)
    #     return dom, response.text

    def get_dom(self):

        """ Получить dom через прокси """

        session = r.Session()
        response = session.get(self.url, headers=self.header)
        print(f'STATUS: {response.status_code}')
        dom = html.fromstring(response.text)
        return dom

    def get_dom_own_ip(self):

        """ Получить dom через свой IP """

        response = r.get(self.url, headers=self.header)
        print(f'STATUS: {response.status_code}')
        dom = html.fromstring(response.text)
        return dom

    @staticmethod
    def set_fake_user_agent(self):

        """  """

        fake_user_agent = None

        with open("user_agents.txt", "r") as file:

            random_number = random.randint(1, 213)

            for i, line in enumerate(file):
                if random_number == i:
                    fake_user_agent = line.replace('\n', '')

        return fake_user_agent

    # def test_ip(self):
    #
    #     """ Проверка IP через сайт 2ip.ru. """
    #
    #     self.header['User-Agent'] = self.fake_user_agent
    #
    #     session = r.Session()
    #     session.proxies = {'http': 'http://77.51.188.76:64053'}
    #     session.auth = HTTPProxyAuth('NyhVuE', 'PaXVEqYK5zYZ')
    #
    #     response = session.get('https://2ip.ru/')
    #
    #     dom = html.fromstring(response.text)
    #     print('ip с сайта 2ip.ru: ', dom.xpath("//div[@class='ip-info']//div[@class='ip']/span/text()")[0])
    #
    #     response = session.get('http://ip-api.com/json')
    #     print('ip с сайта ip-api.com: ', json.loads(response.text)["query"])
    #
    #     response = session.get(self.url)
    #     print(response.text)


if __name__ == '__main__':

    # user_connection = Proxy('https://whoer.net/ru')
    # user_connection.test_ip()

    pass


# 213.87.161.2
# 37.147.251.214


# top100_id=t1.-1.1408381247.1646987061394;
# last_visit=1647244856142::1647255656142;
# t1_sid_-1=s1.2051492064.1647255656139.1647255656144.11.1.18;
# top100_id=t1.-1.1408381247.1646987061394;
# last_visit=1647227008912::1647237808912;
# t1_sid_-1=s1.112089778.1647237808864.1647237808914.6.1.16;
# br=1646987061;
# _ym_uid=1646987061399811319;
# _ym_d=1646987061;
# brjs=1646987061452;
# tmr_lvid=33103beec771d8802c3b56129ff19150;
# tmr_lvidTS=1646987061910;
# top100_id=t1.-1.489026816.1646987428140;
# tmr_lvid=33103beec771d8802c3b56129ff19150;
# tmr_lvidTS=1646987061910; tmr_reqNum=65;
# t1_sid_-1=s1.999313193.1647169823036.1647169823054.4.1.10;
# _ym_isad=2;
# _ym_visorc=w;
# tmr_detect=0|1647255658503;
# tmr_reqNum=69






