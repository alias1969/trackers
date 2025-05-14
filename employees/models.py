from django.db import models
import django_filters

from django.db.models import Count, Min, Q


NULLABLE = {"blank": True, "null": True}


class Employee(models.Model):
    """Модель сотрудники"""

    name = models.CharField(
        max_length=250,
        verbose_name="ФИО",
        help_text="Введите ФИО сотрудника",
    )

    job_title = models.CharField(
        max_length=250,
        verbose_name="должность",
        help_text="Введите должность сотрудника",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.name


