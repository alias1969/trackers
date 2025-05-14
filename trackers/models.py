from django.db import models

from employees.models import Employee

import django_filters
from django.db.models import Q

NULLABLE = {"blank": True, "null": True}


class Tracker(models.Model):
    """Модель задачи"""

    STATUS_CHOICE = [
        ('consideration', 'На рассмотрении'),
        ('active', 'В работе'),
        ('completed', 'Выполнена')
    ]

    title = models.CharField(
        max_length=250,
        verbose_name="Наименование задачи",
        help_text="Введите название задачи",
    )

    description = models.TextField(
        verbose_name="Описание задачи",
        help_text="Введите описание задачи",
        **NULLABLE,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная задача",
        help_text="Укажите связанную задачу",
        **NULLABLE,
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        verbose_name="Исполнитель",
        help_text="Укажите исполнителя",
        **NULLABLE,
    )

    deadline = models.DateTimeField(
        verbose_name="Срок",
        help_text="Укажите срок выполнения",
        **NULLABLE,
    )

   # Статус задачи: consideration, active, completed
    status = models.CharField(
        default='consideration',
        max_length=50,
        choices=STATUS_CHOICE,
        verbose_name="Статус",
        help_text="Укажите статус задачи",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return f'{self.title}: {self.status}'

