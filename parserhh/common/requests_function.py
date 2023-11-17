import requests
from collections import Counter
import os
from datetime import datetime
import sqlite3
import json


def getPage(page, url, name_vacancies):
    params = {
        'text': f'NAME:{name_vacancies}',
        'area': 1,
        'page': page,
        'per_page': 20
    }
    result = requests.get(url, params=params)
    result_decode = result.content.decode()
    result.close()
    return result_decode
def check_time_delta(select_date_create):
    delta = 0
    if select_date_create:
        time_create_records = select_date_create[0][0]
        dt_mow = datetime.now()
        delta = (dt_mow - time_create_records).days
        return delta
    else:
        return delta
def parsingVacancies(list_pages):

    # считываем с каждой страницы вакансии
    list_items_pages = [page.get('items') for page in list_pages]

    # определяем id каждой вакансии на сайте hh.ru
    list_url_id = []
    for items in list_items_pages:
        for item in items:
            list_url_id.append(item.get('url'))
    list_key_skills = []
    for url in list_url_id:
        res_vac_id = json.loads(getVacancies_ID(url))
        value = res_vac_id.get('key_skills')
        list_key_skills.append(value)

    result_list_skills = skills_statistic(list_key_skills)
    return result_list_skills
def getVacancies_ID(url):
    result = requests.get(url)
    result_decode = result.content.decode()
    result.close()
    return result_decode
def skills_statistic(list_key_skills):
    list_all_skills = []
    for skills in list_key_skills:
        if type(skills) == list:
            for skill in skills:
                list_all_skills.append(skill.get('name'))
    sort_skills = Counter(list_all_skills)
    count_skills = len(sort_skills)
    list_sort_key = list(sort_skills)
    dict_skills = dict(sort_skills)
    value_sort_skills = sorted(dict_skills.values())
    value_sort_skills.reverse()
    list_statistic_skills = []
    for count in range(len(list_sort_key)):
        dict_skills = {}
        # value = f'count:{value_sort_skills[count]}, percent:{int(value_sort_skills[count] * 100 / count_skills)}%'
        # dict_skills = {list_sort_key[count]: value}
        interest = int(value_sort_skills[count] * 100 / count_skills)
        # dict_skills = {list_sort_key[count]: value}
        skills_tuple = (list_sort_key[count], interest)
        list_statistic_skills.append(skills_tuple)
    return list_statistic_skills

def averageSalary(list_salary):
    summ = 0
    for i in list_salary:
        summ += i
    average_salary = int(summ / len(list_salary))
    return average_salary


