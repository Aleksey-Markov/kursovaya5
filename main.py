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

companies = []
for company in data['items']:
    if company['open_vacancies'] != 0:
        companies.append(company)


def save_companies_to_json():
    with open('companies.json', 'w', encoding='utf=8') as file:
        json.dump(companies, file, indent=4)


def generate_db():
    conn = psycopg2.connect(
            host='localhost',
            database='headhunter',
            user='postgres',
            password=DBPASS
    )
    cur = conn.cursor()
    # cur.execute('CREATE TABLE company(company_id SERIAL PRIMARY KEY, company_name varchar(25) NOT NULL, company_link text)')
    # cur.execute('CREATE TABLE vacancies(vacancy_id SERIAL PRIMARY KEY, company_id int REFERENCES company(company_id), vacancy_name varchar(100) NOT NULL, vacancy_salary varchar(25), vacancy_city varchar(25))')
    # companies_name = []
    # for comp in companies:
    #     companies_name.append(comp['name'])
    # companies_link = []
    # for comps in companies:
    #     companies_link.append(comps['alternate_url'])
    # cur_insert_comps = 'INSERT INTO company(company_name, company_link) VALUES (%s, %s)'
    # for i in zip(companies_name, companies_link):
    #     cur.execute(cur_insert_comps, i)
    # vacancies = []
    # vacs_name = []
    # vacs_salary = []
    # vacs_city = []
    # with open('companies.json', 'r', encoding='utf=8') as f:
    #     for vac in json.load(f):
    #         vacancies.append(vac['vacancies_url'])
    # num = 0
    # while num != 11:
    #     res = requests.get(vacancies[num])
    #     vac = res.json()['items']
    #     for names in range(len(vac)):
    #         vacs_name.append(vac[names]['name'])
    #     for salarys in range(len(vac)):
    #         vacs_salary.append(f"{vac[salarys]['salary']['from']} {vac[salarys]['salary']['currency']}")
    #     for city in range(len(vac)):
    #         vacs_city.append(vac[city]['area']['name'])
    #     num += 1
    # cur_insert_vacs = 'INSERT INTO vacancies(vacancy_name, vacancy_salary, vacancy_city) VALUES (%s, %s, %s)'
    # for i in zip(vacs_name, vacs_salary, vacs_city):
    #     cur.execute(cur_insert_vacs, i)
    # cur_insert_id = 'INSERT INTO vacancies(company_id) VALUES %s'
    count = []
    for i in range(len(companies)):
        count.append(companies[i]['open_vacancies'])

    # cur.execute()


    conn.commit()
    cur.close()
    conn.close()

generate_db()
# num = 1
# for i in range(len(companies)):
#     count = (companies[i]['open_vacancies'])
#     nums = (str(num) * count)
#     num += 1
# print(nums)
