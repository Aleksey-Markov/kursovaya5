import json

import requests
import psycopg2

params = {'per_page': 100, 'page': 2, 'area': 4}
url = 'https://api.hh.ru/employers/'
response = requests.get(url, params=params)


companies = []
for company in response.json()['items']:
    if company['open_vacancies'] != 0:
        companies.append(company)
with open('companies.json', 'w', encoding='utf=8',) as file:
    json.dump(companies, file, indent=4)
# vacancies = []
# for
#
# conn = psycopg2.connect(
#         host='localhost',
#         database='headhunter',
#         user='postgres',
#         password='83436891'
# )
# cur = conn.cursor()
# cur.execute('CREATE TABLE company(company_id SERIAL PRIMARY KEY, company_name varchar(25) NOT NULL, company_link text)')
# cur.execute('CREATE TABLE vacancies(vacancy_id SERIAL PRIMARY KEY, company_id int REFERENCES company(company_id), vacancy_name varchar(100) NOT NULL, vacancy_salary varchar(25), vacancy_description text)')
# companies_name = []
# for comp in companies:
#     companies_name.append(comp['name'])
# companies_link = []
# for comps in companies:
#     companies_link.append(comps['alternate_url'])
# cur_insert = 'INSERT INTO company(company_name, company_link) VALUES (%s, %s)'
# for i in zip(companies_name, companies_link):
#     cur.execute(cur_insert, i)
#
# conn.commit()
# cur.close()
# conn.close()
