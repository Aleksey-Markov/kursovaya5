import json
import requests
import psycopg2
import os

DBPASS = os.environ['POSTGRESPASS']
url = 'https://api.hh.ru/employers/'


def get_vacs(url):
    params = {'per_page': 100, 'page': 2, 'area': 4}
    response = requests.get(url, params=params)
    return response.json()


data = get_vacs(url)


def get_companies_list(file):
    companies = []
    with open(file, 'r', encoding='utf=8') as file:
        f = json.load(file)
        for company in f:
            if company['open_vacancies'] != 0:
                companies.append(company)
    return companies


companies_list = get_companies_list('companies.json')


def save_companies_to_json(companies_list):
    with open('companies.json', 'w', encoding='utf=8') as file:
        json.dump(companies_list, file, indent=4)


def generate_db(companies_list):
    conn = psycopg2.connect(
            host='localhost',
            database='headhunter',
            user='postgres',
            password=DBPASS
    )
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE companies(company_id int PRIMARY KEY, company_name varchar(25) NOT NULL, company_link text)
        '''
    )
    for comp in companies_list:
        company_id = comp['id']
        company_name = comp['name']
        company_link = comp['alternate_url']
        cur.execute('''
            INSERT INTO companies(company_id, company_name, company_link)
            VALUES (%s, %s, %s)''', (company_id, company_name, company_link)
                    )
    cur.execute(
        '''
        CREATE TABLE vacancies(vacancy_id SERIAL PRIMARY KEY, company_id int NOT NULL ,
        vacancy_name varchar(100) NOT NULL, vacancy_salary varchar(25), vacancy_city varchar(25), vacancy_link text,
        FOREIGN KEY (company_id) REFERENCES companies(company_id))
         '''
    )

    num = 0
    vacancies = []

    with open('companies.json', 'r', encoding='utf=8') as f:
        for vac in json.load(f):
            vacancies.append(vac['vacancies_url'])
    while num != 11:
        res = requests.get(vacancies[num]).json()['items']
        for vac in res:
            for names, company in zip(range(len((vac))), company_id):
                company_id = vac['employer']['id']
                vacs_name = vac['name']
                if vac['salary']['from'] == None:
                    vacs_salary = 'Зарплата не указана'
                else:
                    vacs_salary = f"{vac['salary']['from']} {vac['salary']['currency']}"
                vacs_city = vac['area']['name']
                vacs_link = vac['alternate_url']
            cur.execute('''
            INSERT INTO vacancies(company_id, vacancy_name, vacancy_salary, vacancy_city, vacancy_link)
            VALUES (%s, %s, %s, %s, %s)''',
            (company_id, vacs_name, vacs_salary, vacs_city, vacs_link))
        num += 1

    conn.commit()
    cur.close()
    conn.close()


generate_db(companies_list)
