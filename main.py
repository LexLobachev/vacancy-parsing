from itertools import count
from dotenv import load_dotenv
from terminaltables import AsciiTable

import time
import requests
import os

LANGUAGES = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'Go', 'C#', 'C']


def predict_rub_salary_hh(vac):
    average_salary = None
    if vac['salary'] is None:
        return average_salary
    elif vac['salary']['currency'] != 'RUR':
        return average_salary
    elif vac['salary']['from'] is None:
        average_salary = vac['salary']['to'] * 0.8
    elif vac['salary']['to'] is None:
        average_salary = vac['salary']['from'] * 1.2
    else:
        average_salary = (vac['salary']['to'] - vac['salary']['from'])//2.0
    return average_salary


def predict_rub_salary_sj(super_vac):
    average_salary = None
    if super_vac['currency'] != 'rub':
        return average_salary
    elif (super_vac['payment_from'] is None or super_vac['payment_from'] == 0) and (
            super_vac['payment_to'] is None or super_vac['payment_to'] == 0):
        return average_salary
    elif super_vac['payment_from'] is None or super_vac['payment_from'] == 0:
        average_salary = super_vac['payment_to'] * 0.8
    elif super_vac['payment_to'] is None or super_vac['payment_to'] == 0:
        average_salary = super_vac['payment_from'] * 1.2
    else:
        average_salary = (super_vac['payment_to'] - super_vac['payment_from']) // 2.0
    return average_salary


def sj_salaries_by_lang(secret_key):
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
            if predict_rub_salary_sj(vacancy) is not None:
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


def hh_salaries_by_lang():
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
    print(table.table)


if __name__ == '__main__':
    load_dotenv()
    sj_secret_key = os.environ.get('SJ_SECRET_KEY')
    draw_table(hh_salaries_by_lang(), 'HeadHunter Moscow')
    draw_table(sj_salaries_by_lang(sj_secret_key), 'SuperJob Moscow')
