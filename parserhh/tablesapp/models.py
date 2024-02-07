from django.db import models



# Create your models here.
class Vacancy(models.Model):
    name_vacancies = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name_vacancies


class Skill(models.Model):
    name_skills = models.CharField(max_length=64, unique=True)
    vacancies = models.ManyToManyField(Vacancy, through="VacancySkill")

    def __str__(self):
        return self.name_skills


class VacancySkill(models.Model):
    vacancies = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    key_skills = models.ForeignKey(Skill, on_delete=models.CASCADE)
    statistics = models.IntegerField()
    date_recording = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['vacancies', 'key_skills'],
                name='unique_vacancy_skill'
            ),
        ]
