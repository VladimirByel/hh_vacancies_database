from exceptions import ParsingError
from abc import ABC, abstractmethod
import requests
import os

HH = "https://api.hh.ru/vacancies"
json_hh = "hh_vacancies.json"
HH_PATH = os.path.abspath(json_hh)

class Api(ABC):
    pass


class APIhh(Api):
    url = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.key = ""
        self.vacancies = []
        self.headers = {
            "HH-User-Agent": self.key
        }
        self.params = {
            "per_page": 100,
            "page": 0,
            "archived": False,
            "employer_id": None
        }

    def get_request(self):
        response = requests.get(url=self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! {response.status_code}")
        return response.json()['items']

    def get_vacancies(self, employer_id, pages_count=3):
        vacancies = []  # очищаем список вакансий
        for page in range(pages_count):
            page_vacancies = []
            self.params['page'] = page
            self.params['employer_id'] = employer_id
            print(f'({self.__class__.__name__}) Парсинг страницы {page} -', end=' ')
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                vacancies.extend(page_vacancies)
                print(f'Загружено вакансий (employer_id {employer_id}): {len(page_vacancies)}')
            if len(page_vacancies) == 0:
                break

        return vacancies
