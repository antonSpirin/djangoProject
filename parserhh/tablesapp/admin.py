from django.contrib import admin
from .models import Vacancy, Skill, VacancySkill

admin.site.register (Vacancy)
admin.site.register (Skill)
admin.site.register (VacancySkill)

# Register your models here.