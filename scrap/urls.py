from django.urls import path

from .views import home_view, Vacancy_List

urlpatterns = [
    path('', home_view, name='home'),
    path('list', Vacancy_List.as_view(), name='list')
]