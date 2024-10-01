from django.contrib.auth.models import User
from django.core import validators
from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=64, verbose_name='Кличка животного')
    color = models.CharField(max_length=64, verbose_name='Окрас животного')
    description = models.CharField(max_length=512,
                                   verbose_name='Краткое описание животного')
    age = models.PositiveIntegerField(verbose_name='Возраст в месяцах')
    breed = models.ForeignKey('Breed',
                              on_delete=models.CASCADE,
                              related_name='cats',
                              verbose_name='Порода животного')
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='cats',
                              verbose_name='Владелец животного')
    rating = models.FloatField(default=0, verbose_name='Рейтинг животного')

    def __str__(self):
        return f'{self.name} породы {self.breed}'

    class Meta:
        verbose_name = 'Кошка'
        verbose_name_plural = 'Кошки'


class Breed(models.Model):
    name = models.CharField(unique=True, max_length=128, verbose_name='Порода животного')
    description = models.CharField(max_length=512, verbose_name='Описание породы', blank=True)

    def __str__(self):
        return f'Порода {self.name}'

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'


class Vote(models.Model):
    value = models.PositiveSmallIntegerField(verbose_name='Оценка',)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cat = models.ForeignKey('Cat', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.value} за {self.cat.name}'
    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        unique_together = ('user', 'cat')
