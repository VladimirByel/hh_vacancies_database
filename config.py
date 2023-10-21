import os

HH = "https://api.hh.ru/vacancies"
KEY = os.getenv(key)
json_hh = "hh_vacancies.json"
HH_PATH = os.path.abspath(json_hh)