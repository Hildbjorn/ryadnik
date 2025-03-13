from django.db import models
from django.utils import timezone

class Tag(models.Model):
    """ Модель стягов (тегов) """

    COLOR_CHOICES = [
        ('primary', 'Основной'),
        ('success', 'Успешный'),
        ('danger', 'Опасный'),
        ('warning', 'Тревожный'),
        ('secondary', 'Второстепенный'),
    ]

    name = models.CharField(max_length=50,
                            verbose_name='Стяг')

    color = models.CharField(max_length=20,
                             choices=COLOR_CHOICES,
                             default='primary')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Стяг'
        verbose_name_plural = 'Стяги'
        ordering = ['name']


class Task(models.Model):
    """ Модель дел """

    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Обычный'),
        ('high', 'Высокий'),
    ]

    title = models.CharField(max_length=200,
                             verbose_name='Заголовок')

    description = models.TextField(blank=True,
                                   verbose_name='Описание')

    due_date = models.DateTimeField(null=True,
                                    blank=True,
                                    verbose_name='Срок исполнения')

    status = models.BooleanField(default=False,
                                 verbose_name='Статус')

    priority = models.CharField(max_length=10,
                                choices=PRIORITY_CHOICES,
                                default='medium',
                                verbose_name='Приоритет')

    tags = models.ManyToManyField(Tag,
                                  blank=True,
                                  verbose_name='Стяги')

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')

    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Дело'
        verbose_name_plural = 'Дела'
        ordering = ['-due_date']