from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status

from datetime import date

from employees.models import Employee
from trackers.models import Tracker


class EmployeeTest(APITestCase):
    """Тест модели сотрудников"""

    def setUp(self):
        """Тестовые данные"""

        Employee.objects.all().delete()
        Tracker.objects.all().delete()

        self.user = User.objects.create(username="test")
        self.employee = Employee.objects.create(name="Иванов Петр Васильевич")
        self.tracker = Tracker.objects.create(
            title="Test", description="test", deadline=date.today()
        )

        self.client.force_authenticate(user=self.user)

    def test_employee_create(self):
        """Тестирование создание сотрудника"""

        data = {
            "name": "Новый сотрудник",
            "job_title": "Новая должность",
        }
        response = self.client.post("/employee/", data=data)
        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_employee_list(self):
        """Тест списка всех сотрудников"""

        url = reverse("employees:employee-list")
        response = self.client.get(url)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        # Сверяем данные
        self.assertEqual(
            data,
            [
                {
                    "id": self.employee.id,
                    "name": "Иванов Петр Васильевич",
                    "job_title": None,
                    "tracker_count": 0,
                }
            ],
        )

        # Сверяем ожидаемое количество Employee
        self.assertEqual(Employee.objects.count(), 1)

    def test_employee_retrieve(self):
        """Тест детальной информации о сотруднике"""

        url = reverse("employees:employee-detail", args=(self.employee.pk,))
        response = self.client.get(url)
        data = response.json()

        # Сверяем данные
        self.assertEqual(
            data,
            {
                "id": self.employee.id,
                "name": "Иванов Петр Васильевич",
                "job_title": None,
                "tracker_count": 0,
            },
        )

    def test_employee_update(self):
        """Тестирование обновление данных о сотруднике"""

        url = reverse("employees:employee-detail", args=(self.employee.pk,))

        data = {
            "name": "Новое имя",
        }
        response = self.client.patch(url, data=data)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сверяем данные
        self.assertEqual(response.json()["name"], "Новое имя")

    def test_employee_delete(self):
        """Тестирование удаление сотрудника"""

        url = reverse("employees:employee-detail", args=(self.employee.pk,))

        response = self.client.delete(url)

        # Сверяем статус код
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Сверяем количество Employee
        self.assertEqual(Employee.objects.count(), 0)
