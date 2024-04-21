
import psycopg2


class DBManager:
    def __init__(self, connection):
        self.connection = connection
        self.cur = conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute('''SELECT company_name, COUNT(vacancy_id) AS vacancy_count
                FROM companies
                JOIN vacancies
                USING (company_id)
                GROUP BY company_name''')
        companies_and_vacs_count = self.cur.fetchall()
        return companies_and_vacs_count

    def get_all_vacancies(self):
        self.cur.execute('''SELECT company_name, vacancy_name, vacancy_salary, vacancy_link
                FROM vacancies
                JOIN companies
                USING (company_id)''')
        vacs = self.cur.fetchall()
        return vacs

    def get_avg_salary(self):
        self.cur.execute('''SELECT AVG(vacancy_salary)::DECIMAL(10, 2)
                FROM vacancies''')
        salary = self.cur.fetchall()
        return salary[0][0]

    def get_vacancies_with_higher_salary(self):
        self.cur.execute('''SELECT * 
                        FROM vacancies
                        WHERE vacancy_salary > (
                        SELECT AVG(vacancy_salary)
                        FROM vacancies)''')
        high_salary = self.cur.fetchall()
        return high_salary

    def get_vacancies_with_keyword(self, keyword):
        self.keyword = keyword
        self.cur.execute("""SELECT *
                FROM vacancies
                WHERE (vacancy_name) LIKE '%{self.keyword}%'""")
        keyvacs = self.cur.fetchall()
        return keyvacs


conn = psycopg2.connect(
            host='localhost',
            database='headhunter',
            user='postgres',
            password=83436891
    )
hh = DBManager(conn)
