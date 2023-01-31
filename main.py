from itertools import count
from dotenv import load_dotenv
from terminaltables import AsciiTable

import time
import requests
import os

LANGUAGES = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'Go', 'C#', 'C']


def salary_by_condition(salary_currency, salary_from, salary_to):
    average_salary = None
    if salary_currency != 'RUR' or salary_currency != 'rub':
        return average_salary
    elif not salary_from and not salary_to:
        return average_salary
    elif not salary_from:
        average_salary = salary_to * 0.8
    elif not salary_to:
        average_salary = salary_from * 1.2
    else:
        average_salary = (salary_to - salary_from)//2.0
    return average_salary


def predict_rub_salary_hh(vac):
    hh_salary_currency = vac['salary']['currency']
    hh_salary_from = vac['salary']['from']
    hh_salary_to = vac['salary']['to']
    return salary_by_condition(hh_salary_currency, hh_salary_from, hh_salary_to)


def predict_rub_salary_sj(super_vac):
    sj_salary_currency = super_vac['currency']
    sj_salary_from = super_vac['payment_from']
    sj_salary_to = super_vac['payment_to']
    return salary_by_condition(sj_salary_currency, sj_salary_from, sj_salary_to)


def get_sj_salaries_by_lang(secret_key):
    count_vacancies = {}
    for lang in LANGUAGES:
        vacancies = []
        vac_found = 0
        vac_processed = 0
        total_salary = 0
        for page in count(0):
            url = 'https://api.superjob.ru/2.0/vacancies/'
            params = {
                'keyword': lang,
                'town': 4,
                'page': page,
                'app_key': secret_key
            }
            page_response = requests.get(url, params=params)
            page_response.raise_for_status()

            page_payload = page_response.json()
            vac_found = page_payload['total']
            vacancies += page_payload['objects']
            time.sleep(0.25)
            if not page_payload['more']:
                break

        for vacancy in vacancies:
            if predict_rub_salary_sj(vacancy):
                total_salary += predict_rub_salary_sj(vacancy)
                vac_processed += 1
        if vac_processed != 0:
            av_salary = total_salary // vac_processed
        else:
            av_salary = 0
        count_vacancies[lang] = {
            "vacancies_found": vac_found,
            "vacancies_processed": int(vac_processed),
            "average_salary": int(av_salary)
        }
    return count_vacancies


def get_hh_salaries_by_lang():
    count_vacancies = {}
    for lang in LANGUAGES:
        vacancies = []
        vac_found = 0
        for page in count(0):
            params = {
                'text': f'NAME:Программист {lang}',
                'area': 1,
                'search_period': 30,
                'per_page': 100
            }
            page_response = requests.get('https://api.hh.ru/vacancies', params)
            page_response.raise_for_status()

            page_payload = page_response.json()
            vac_found = page_payload['found']
            if page >= page_payload['pages']:
                break

            vacancies += page_payload['items']
            time.sleep(0.25)

        if vac_found > 100:
            vac_processed = 0
            total_salary = 0
            for vacancy in vacancies:
                if predict_rub_salary_hh(vacancy) is not None:
                    vac_processed += 1
                    total_salary += predict_rub_salary_hh(vacancy)
            av_salary = total_salary // vac_processed
            count_vacancies[lang] = {
                "vacancies_found": vac_found,
                "vacancies_processed": int(vac_processed),
                "average_salary": int(av_salary)
            }
    return count_vacancies


def draw_table(vacancies_statistics, header):
    salary_statistics = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]
    for language in vacancies_statistics.keys():
        language_salary = vacancies_statistics[language]
        salary_statistics.append(
            [
                language,
                language_salary['vacancies_found'],
                language_salary['vacancies_processed'],
                language_salary['average_salary']
            ]
        )
    table = AsciiTable(salary_statistics, header)
    return table.table


if __name__ == '__main__':
    load_dotenv()
    sj_secret_key = os.environ.get('SJ_SECRET_KEY')
    print(draw_table(get_hh_salaries_by_lang(), 'HeadHunter Moscow'))
    print(draw_table(get_sj_salaries_by_lang(sj_secret_key), 'SuperJob Moscow'))
