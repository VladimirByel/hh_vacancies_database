import psycopg2
from utils import get_employers
from DBManager import DBManager
from api import APIhh, HH
from exceptions import ConfigException


def main():
    employers = []
    vacancies = []
    try:
        db_manager = DBManager()
        db_manager.create_database()
        db_manager.create_tables()
    except FileNotFoundError:
        FileNotFoundError('Ошибка: файл не найден')
    #    exit()
    """
    except ConfigException:
        print("Ошибка конфигурации")
        exit()
    except psycopg2.Error:
        print('Ошибка инициализации базы данных')
        exit()
        
        """

    # заполнение таблицы employers
    employers = get_employers()
    db_manager.fill_employers(employers)
    """
    try:
        employers = get_employers()
        db_manager.fill_employers(employers)
    except FileNotFoundError:
        FileNotFoundError('Файл не найден')
    except Exception:
        print("boom")
    #    exit()
    """

    # парсинг вакансий (hh.ru)
    hh = APIhh()
    for employer_id in employers.values():
        vacancies.extend(hh.get_vacancies(employer_id))

    # заполнение таблицы vacancies
    db_manager.fill_vacancies(vacancies)

    # вывод результатов запросов
    while True:
        user_input = input("""
1 - вывести все вакансии
2 - получить зреднюю зарплату
exit - завершить работу\n""")
        if user_input == '1':
            vacancies = db_manager.get_vacancies()
            for vacancy in vacancies:
                print(vacancy)
        elif user_input == '2':
            vacancy = db_manager.get_avg_salary()
            #for vacancy in vacancies:
            rounded_vacancy = round(vacancy)
            print(rounded_vacancy)
        elif user_input == 'exit':
            break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
