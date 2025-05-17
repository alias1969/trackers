from rest_framework import serializers
from employees.models import Employee
from trackers.serializers import TrackerSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Employee"""

    # Вывод поля tracker_count только для чтения
    tracker_count = serializers.IntegerField(read_only=True)
    trackers = TrackerSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "name", "job_title", "tracker_count", "trackers"]
