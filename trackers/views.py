from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from employees.models import Employee
from trackers.models import Tracker
from trackers.filters import TrackerFilter
from trackers.serializers import TrackerSerializer


class TrackerViewSet(viewsets.ModelViewSet):
    """ViewSet для модели TRACKER"""

    queryset = Tracker.objects.all()
    serializer_class = TrackerSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = TrackerFilter
    ordering_fields = ("id", "status")

    def list(self, request, *args, **kwargs):
        """Вывод задач по ТЗ"""

        queryset = self.filter_queryset(self.get_queryset())
        serializer = TrackerSerializer(queryset, many=True)

        # Параметры фильтрации в поисковой строке
        filter_params = request.query_params

        # Фильтр по важным задачам
        if filter_params.get("important_trackers"):

            response = []

            for item in serializer.data:

                # получим имя исполителя задачи
                employee_id = item["employee"]
                employee_info = Employee.objects.filter(id__in=employee_id)
                employee_name = [employee.name for employee in employee_info]

                # Создаем необходимый формат ответа
                response.append(
                    {
                        "Важная задача": item["title"],
                        "Срок": item["deadline"],
                        "Сотрудник": employee_name,
                    }
                )

            return Response(response)

        return Response(serializer.data)
