import psycopg2
import requests

class APIhh:

    def __init__(self, url, text):
        self.url = url
        self.key = ""
        self.text = text

    def getting_info(self):
        payload = {}
        headers = {
            "User_Agent": ''
        }

        vacancies = []
        for page in range(2):
            params = {
                "per_page": 50,
                "page": page,
                "text": self.text
            }
            response = requests.request("GET", self.url, headers=headers, data=payload, params=params)
            json_response = response.json()
            vacancies.extend(json_response['items'])
            if json_response["pages"] - 1 == page:
                break
        return {
            "items": vacancies
        }

class DBManager:

    def get_companies_and_vacancies_count(self):
        pass
"""получает список всех компаний и количество вакансий у каждой компании."""

    def get_all_vacancies(self):
        pass
"""получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""

    def get_avg_salary(self):
        pass
"""получает среднюю зарплату по вакансиям."""

    def get_vacancies_with_higher_salary(self):
        pass
"""получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

    def get_vacancies_with_keyword(self):
        pass
"""получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
