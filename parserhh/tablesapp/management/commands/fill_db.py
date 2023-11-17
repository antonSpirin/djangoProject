from django.core.management.base import BaseCommand
from tablesapp.models import Vacancy, Skill, VacancySkill
from common.requests_function import getPage, parsingVacancies
from sqlite3 import IntegrityError
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        # добавляем данные в таблицы
        key_vacancy = input('Введите назавание вакансии для поиска: ')
        vacancy, created = Vacancy.objects.get_or_create(name_vacancies=key_vacancy)
        # try:
        #     customer = Customer.objects.get(username="janedoe", email="janedoe@gmail.com")
        #     print(customer)
        # except Customer.DoesNotExist:
        #     customer = Customer(username="janedoe", email="janedoe@gmail.com")
        #     customer.save()

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

        #     list_obj_skills.append(skill)
        # Key_skills.objects.bulk_create(list_obj_skills, ignore_conflicts=True)

        # получим список данных из таблицы для того что бы узнать id каждого значения skills
        # list_skills_id = []
        # skills_query = Key_skills.objects.all()
        # for skill_obj in skills_query:
        #     list_skills_id.append([skill_obj.id, skill_obj.name_skills])

        # подготовим список для заполнения итоговой таблицы в базе данных

        # count = 0
        # for row in skills_query:
        #     # skill_id = 0
        #     # for skill in list_skills_id:
        #     #     if row.name_skills == skill[1]:
        #     #         skill_id = skill[0]
        #     # count = skills_query.index(row)
        #     statistic_skill = int(result_list_skills[count][1])
        #     Vacancy_key_skills.objects.get_or_create(vacancies=vacansy.pk, key_skills=row.pk, statistics=statistic_skill)
        #     count += 1

        # result_obj = Vacancy_key_skills(vacancies_id, skill_id, statistic_skill)
        # list_insert_date.append(result_obj)
        # print(list_insert_date)
        # Vacancy_key_skills.objects.bulk_create(list_insert_date,ignore_conflicts=True)
