import os
import sys
import django
import datetime

from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model

direct = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(direct)
os.environ['DJANGO_SETTINGS_MODULE'] = 'job_scrapping.settings'

django.setup()

from scrap.models import Vacancy, Error
from job_scrapping.settings import EMAIL_HOST_USER

ADMIN_EMAIL = EMAIL_HOST_USER
today = datetime.date.today()
subject = f'Рассылка вакансий за {today}'
text_content = f'Рассылка вакансий за {today}'
from_email = EMAIL_HOST_USER

empty = '<h2>К сожалению, вакансий по вашим критериям сегодня не найдено</h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for q in qs:
    users_dict.setdefault((q['city'], q['language']), [])
    users_dict[(q['city'], q['language'])].append(q['email'])

if users_dict:
    params = {
        'city_id__in': [],
        'language_id__in': []
    }
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()[:10]
    vacancies = {}
    for q in qs:
        vacancies.setdefault((q['city_id'], q['language_id']), [])
        vacancies[(q['city_id'], q['language_id'])].append(q)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h5><a href="{row["url"]}">{row["title"]}</a></h5>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

qs = Error.objects.filter(timestamp=today)
if qs.exists():
    subject = 'В работе сервиса обнаружена ошибка!'
    text_content = 'В работе сервиса обнаружена ошибка!'
    to = ADMIN_EMAIL
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
