from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView

from .models import Vacancy
from .forms import FindForm


def home_view(request):
    form = FindForm()

    return render(request, 'scrap/home.html', {'form': form})


class Vacancy_List(ListView):
    model = Vacancy
    template_name = 'scrap/list.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вакансии'
        context['form'] = FindForm()
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []

        if city or language:
            qs_filter = {}
            if city:
                qs_filter['city__slug'] = city
            if language:
                qs_filter['language__slug'] = language

            qs = Vacancy.objects.filter(**qs_filter).select_related('city', 'language')

        return qs
