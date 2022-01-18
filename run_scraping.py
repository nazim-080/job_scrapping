import os
import asyncio
import sys
import datetime
import django
from django.contrib.auth import get_user_model
from django.db import DatabaseError

direct = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(direct)
os.environ['DJANGO_SETTINGS_MODULE'] = 'job_scrapping.settings'

django.setup()

from scrap.parsers import hh, avito
from scrap.models import Vacancy, Error, Url

User = get_user_model()

parsers = (
    (hh, 'hh'),
    (avito, 'avito'),
)

jobs = []
errors = []


async def main(value):
    func, url, city, language = value
    job, error = await loop.run_in_executor(None, func, url, city, language)
    jobs.extend(job)
    errors.extend(error)


url_list = Url.objects.all().values()

loop = asyncio.get_event_loop()
tmp_task = [(func, data['url_data'][key], data['city_id'], data['language_id'])
            for data in url_list
            for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_task])

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    e = Error(data=errors).save()

week_ago = datetime.date.today() - datetime.timedelta(7)
Vacancy.objects.filter(timestamp__lte=week_ago).delete()