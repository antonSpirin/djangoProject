import pprint
from django.core.management.base import BaseCommand
from tablesapp.models import Vacancy, Skill, VacancySkill
from common.requests_function import getPage, parsingVacancies
from sqlite3 import IntegrityError
import json


class Command(BaseCommand):

    def __init__(self, key_vacancy):
        super().__init__()
        self.vac = key_vacancy
        # self.pages = pages

    def handle(self, *args, **options):
        result = parser_hh(self.vac)
        pprint.pprint(result)


def parser_hh(key_vacancy):
    # добавляем данные в таблицы
    quеry_vacancy = Vacancy.objects.get(name_vacancies=key_vacancy)
    if not quеry_vacancy:
        vacancy, created = Vacancy.objects.get_or_create(name_vacancies=key_vacancy)
        # ищем вакансии по заданным параметрам и записываем результат в базу данных
        DOMAIN = 'https://api.hh.ru/'
        url_vacancies = f'{DOMAIN}vacancies'
        result_list_skills = []
        if not result_list_skills:
            list_pages = []
            for i in range(10):
                res_pages = json.loads(getPage(i, url_vacancies, key_vacancy))
                list_pages.append(res_pages)
            # получаем вакансии и skills
            result_list_skills = parsingVacancies(list_pages)
            list_skills = []
            for skill_stat in result_list_skills:
                list_skills.append(skill_stat[0])
            print(list_skills)

            # добавим skills v таблицу
            for skill in list_skills:
                # Key_skills.objects.get_or_create(name_skills=skill)
                count = list_skills.index(skill)
                obj_skill, created = Skill.objects.get_or_create(name_skills=skill)

                statistic_skill = int(result_list_skills[count][1])
                VacancySkill.objects.get_or_create(vacancies=vacancy, key_skills=obj_skill,
                                                   statistics=statistic_skill)
            print('Данные в итоговую таблицу добавлены')
        else:
            print(f'Данные по вакансии {key_vacancy} есть в базе, выдаем результат из базы данных.')
