from django.db import models


def default_urls():
    return {
        'hh': '',
        'avito': ''
    }


class City(models.Model):
    name = models.CharField("Название", max_length=50, unique=True)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Населенный пункт"
        verbose_name_plural = "Населенные пункты"


class Language(models.Model):
    name = models.CharField("Язык программирования",
                            max_length=50,
                            unique=True)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Язык программирования"
        verbose_name_plural = "Языки программирования"


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-timestamp']


class Url(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    url_data = models.JSONField(default=default_urls)

    def __str__(self):
        return f'{self.city}. {self.language}'

    class Meta:
        unique_together = ('city', 'language')


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.timestamp)
