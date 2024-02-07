from django.shortcuts import render
from .forms import searchForm
from .models import VacancySkill, Vacancy, Skill
from tablesapp.management.commands.fill_db import Command


# Create your views here.
def main_view(request):
    return render(request, 'tablesapp/index.html')


def search_skills(request):
    form_s = searchForm
    return render(request, 'tablesapp/search-skills.html', context={'form': form_s})


def results(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            vac = form.cleaned_data['vacancy']
            print(vac, sep='\n')
            com1 = Command(vac)
            com1.handle()
            vac_obj = Vacancy.objects.get(name_vacancies=vac)
            skills_obj = VacancySkill.objects.filter(vacancies=vac_obj.id).all()
            return render(request, 'tablesapp/results.html', context={'name_vacancy': vac, 'skills': skills_obj})
        else:
            form_s = searchForm
            return render(request, 'tablesapp/results.html', context={'form': form_s})
