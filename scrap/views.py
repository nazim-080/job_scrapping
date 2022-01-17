from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Vacancy
from .forms import FindForm


def home_view(request):
    form = FindForm()

    return render(request, 'scrap/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {
        'city': city,
        'language': language,
        'form': form
    }
    if city or language:
        qs_filter = {}
        if city:
            qs_filter['city__slug'] = city
        if language:
            qs_filter['language__slug'] = language

        qs = Vacancy.objects.filter(**qs_filter)

        paginator = Paginator(qs, 15)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scrap/list.html', context=context)
