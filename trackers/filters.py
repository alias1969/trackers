import django_filters
from django.db.models import Count, Min, Q

from employees.models import Employee
from trackers.models import Tracker

class EmployeeFilter(django_filters.FilterSet):
    """Фильтры по сотрудникам"""

    # Фильтрация сотрудника по количеству задач по убыванию
    count_lte = django_filters.NumberFilter(field_name='tracker_count', lookup_expr='lte')

    # фильтр для получения сотрудников которые выполняют одну из связанных задач или имеют загруженность по
    # задачам максимум на 2 больше от самого разгруженного сотрудника
    employee_for_task = django_filters.BooleanFilter(method='filter_employee_for_task')

    class Meta:
        model = Employee
        fields = ('count_lte', 'employee_for_task')

    def filter_employee_for_task(self, queryset, name, value):
        """ Фильтр для сотрудников для выбора в задаче """

        # Получаем минимальное количество задач
        min_tracker_count = queryset.annotate(tracker_count=Count('trackers')).aggregate(
            Min('tracker_count'))['tracker_count__min']

        # Сотрудники с минимальным количеством задач
        employees_min_tracker_count  = queryset.filter(tracker_count__lte=min_tracker_count)

        # Сотрудники, у которых есть родительская задача и количество задач <= min + 2
        employees_in_parent = queryset.filter(Q(trackers__parent__isnull=False) & Q(tracker_count__lte=min_tracker_count + 2))

        # Объединяем результаты
        return queryset.filter(Q(pk__in=employees_min_tracker_count) | Q(pk__in=employees_in_parent ))


class TrackerFilter(django_filters.FilterSet):
    """Фильтры для задач"""

    # отбор по статусу
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")

    # отбор по наличию связанной задачи
    tracker_with_parent = django_filters.BooleanFilter(field_name="parent", lookup_expr="isnull")

    # отбор по статусу связанной задачи
    related_tracker_status = django_filters.CharFilter(field_name="parent__status", lookup_expr="exact")

    # Отбор по важным задачам: не взяты в работу, но есть связанная задача в работе
    important_trackers = django_filters.BooleanFilter(method='filter_important_trackers')

    class Meta:
        model = Tracker
        fields = ['status', 'important_trackers']

    def filter_important_trackers(self, queryset, name, value):
        """ Вывод важных задач """

        # Отбор по статусу consideration (На рассмотрении) и статусу active связанной задачи
        return queryset.filter(Q(status="consideration") & Q(parent__status='active'))