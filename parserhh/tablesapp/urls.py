from django.urls import path
from tablesapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tablesapp'

urlpatterns = [
    path('', views.main_view, name='index'),
    path('search-skills/', views.search_skills, name='search'),
    path('results/', views.results, name='results')
]
