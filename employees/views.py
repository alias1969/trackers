from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from trackers.filters import EmployeeFilter
from employees.models import Employee
from employees.serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для Employee"""

    queryset = Employee.objects.annotate(tracker_count=Count("tracker"))
    serializer_class = EmployeeSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = EmployeeFilter
    ordering_fields = ("tracker_count", "id")
