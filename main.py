import requests


params = {'per_page': 100, 'page': 2, 'area': 4}

response = requests.get('https://api.hh.ru/employers/', params=params)
# print(response.json())


# vacs = []
# for vac in response.json()['items']:
#     if vac['open_vacancies'] != 0:
#         vacs.append(vac)
# print(vacs)