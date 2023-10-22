import psycopg2
from configparser import ConfigParser


class DBManager:

    def __init__(self):
        self.__config = self.__get_config()

    @staticmethod
    def __get_config(filename="database.ini", section="postgresql"):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(
                'Section {0} is not found in the {1} file.'.format(section, filename))
        return db

    def __execute(self, query):
        connection = psycopg2.connect(**self.__config)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.close()

    def __insert_many(self, query, values):
        connection = psycopg2.connect(**self.__config)
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.executemany(query, values)
        connection.close()

    def __fetch_all(self, query):
        connection = psycopg2.connect(**self.__config)

        with connection.cursor() as cursor:
            cursor.execute(query)
            values = cursor.fetchall()
        connection.close()

        return values

    def create_database(self) -> None:
        config = self.__config.copy()
        config['dbname'] = 'postgres'

        connection = psycopg2.connect(**config)
        connection.autocommit = True

        with connection.cursor() as cursor:
            query = f'DROP DATABASE IF EXISTS {self.__config["dbname"]}'
            cursor.execute(query)
            query = f'CREATE DATABASE {self.__config["dbname"]}'
            cursor.execute(query)

        connection.close()
        print(f"База данных {self.__config['dbname']} создана")

    def create_tables(self) -> None:
        query = """
CREATE TABLE employers (
    employer_id INT PRIMARY KEY,
    title VARCHAR(50)
);
"""
        self.__execute(query)
        print('Таблица employers создана')

        query = """
CREATE TABLE vacancies (
    vacancy_id INT PRIMARY KEY,
    title VARCHAR(100),
    employer_id INT REFERENCES employers (employer_id),
    salary_min FLOAT,
    url VARCHAR(100)
);
        """
        self.__execute(query)
        print("Таблица vacancies создана")

    def fill_employers(self, values):
        employers = [(value, key) for key, value in values.items()]
        query = f"""
INSERT INTO employers ("employer_id", "title")
VALUES
(%s, %s)
        """
        self.__insert_many(query, employers)

    def fill_vacancies(self, values):
        vacancies = []
        for vacancy in values:
            if vacancy['salary']:
                if vacancy['salary']['from']:
                    salary_min = vacancy['salary']['from']
            else:
                salary_min = 0
            vacancies.append((
                vacancy['id'],
                vacancy['name'],
                vacancy['employer']['id'],
                salary_min,
                vacancy['alternate_url']
            ))

        query = """
INSERT INTO vacancies ("vacancy_id", "title", "employer_id", "salary_min", "url")
VALUES
(%s, %s, %s, %s, %s)
        """
        self.__insert_many(query, vacancies)

    def get_vacancies(self):
        query = """
SELECT 
    vacancies.title,
    employers.title AS employer,
    salary_min,
    url
FROM vacancies
JOIN employers USING (employer_id)
        """
        values = self.__fetch_all(query)
        return values

    def get_avg_salary(self):
        query = """
SELECT AVG(salary_min)
FROM vacancies
        """
        values = self.__fetch_all(query)[0][0]
        return values

    def get_vacancies_with_higher_salary(self):
        query = """
SELECT *
FROM vacancies
WHERE salary_min > (SELECT AVG(salary_min) FROM vacancies)
        """
        values = self.__fetch_all(query)
        return values

    def get_vacancies_with_keyword(self, keyword):
        query = f"""
SELECT *
FROM vacancies
WHERE title LIKE '%{keyword}%'
        """
        values = self.__fetch_all(query)
        return values